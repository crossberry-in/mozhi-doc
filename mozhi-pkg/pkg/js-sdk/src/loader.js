// loader.js — JavaScript module loader for Mozhi
// Loads ESM, CommonJS, and Node builtins
// Caches loaded modules for identity preservation

const fs = require('fs');
const path = require('path');
const vm = require('vm');
const resolver = require('./resolver');
const value = require('./value');

// Module cache: path → { exports, type }
const moduleCache = new Map();

// ── Main load function ────────────────────────────────────

async function load(specifier, fromPath) {
  // Check cache first
  if (moduleCache.has(specifier)) {
    return moduleCache.get(specifier);
  }

  // Resolve the specifier to a file path
  const resolved = resolver.resolve(specifier, fromPath || process.cwd());

  let mod;
  switch (resolved.type) {
    case 'builtin':
      mod = loadBuiltin(resolved);
      break;
    case 'file':
    case 'package':
      mod = await loadFile(resolved.path);
      break;
    default:
      throw new Error(`Unknown module type: ${resolved.type}`);
  }

  moduleCache.set(specifier, mod);
  return mod;
}

// ── Node builtins ─────────────────────────────────────────

function loadBuiltin(resolved) {
  const name = resolved.path;
  try {
    const mod = require(name);
    return {
      type: 'builtin',
      exports: flattenExports(mod),
      default: mod.default || mod,
    };
  } catch (e) {
    throw new Error(`Failed to load builtin "${name}": ${e.message}`);
  }
}

// ── File loader (ESM + CJS) ──────────────────────────────

async function loadFile(filePath) {
  if (moduleCache.has(filePath)) {
    return moduleCache.get(filePath);
  }

  const ext = path.extname(filePath);
  const content = fs.readFileSync(filePath, 'utf-8');

  let mod;

  if (ext === '.mjs' || (ext === '.js' && isESM(content))) {
    mod = await loadESM(filePath, content);
  } else {
    mod = loadCJS(filePath, content);
  }

  moduleCache.set(filePath, mod);
  return mod;
}

// ── ESM loader ────────────────────────────────────────────

async function loadESM(filePath, content) {
  // Parse export statements to build exports object
  const exports = {};
  let hasDefault = false;

  // Extract named exports
  const namedExportRegex = /export\s+(?:function|const|let|var|class)\s+(\w+)/g;
  let match;
  while ((match = namedExportRegex.exec(content)) !== null) {
    exports[match[1]] = undefined; // Will be filled after execution
  }

  // Extract export list: export { a, b, c }
  const exportListRegex = /export\s*\{([^}]+)\}/g;
  while ((match = exportListRegex.exec(content)) !== null) {
    const names = match[1].split(',').map(s => s.trim().split(/\s+as\s+/).pop());
    for (const name of names) {
      if (name === 'default') hasDefault = true;
      else exports[name] = undefined;
    }
  }

  // Check for default export
  if (/export\s+default\s/.test(content)) {
    hasDefault = true;
  }

  // Execute in a sandbox to capture exports
  const moduleDir = path.dirname(filePath);
  const sandbox = createSandbox(filePath);

  // Transform ESM to runnable code
  const transformed = transformESM(content, filePath);

  try {
    const script = new vm.Script(transformed, { filename: filePath });
    const context = vm.createContext(sandbox);
    const result = script.runInContext(context);

    // Collect exports from sandbox
    const finalExports = {};
    // Use module.exports keys (most reliable after transformation)
    const modExports = sandbox.module?.exports || {};
    for (const key of Object.keys(modExports)) {
      finalExports[key] = modExports[key];
    }
    // Also check sandbox globals (for non-module exports)
    for (const key of Object.keys(exports)) {
      if (finalExports[key] === undefined) {
        if (sandbox[key] !== undefined) {
          finalExports[key] = sandbox[key];
        }
      }
    }

    return {
      type: 'esm',
      exports: finalExports,
      default: sandbox.__default || sandbox.module?.exports?.default || result,
    };
  } catch (e) {
    throw new Error(`Failed to load ESM module "${filePath}": ${e.message}`);
  }
}

// ── CJS loader ────────────────────────────────────────────

function loadCJS(filePath, content) {
  const sandbox = createSandbox(filePath);

  try {
    const script = new vm.Script(content, { filename: filePath });
    const context = vm.createContext(sandbox);
    script.runInContext(context);

    const exports = flattenExports(sandbox.module.exports);
    return {
      type: 'cjs',
      exports,
      default: sandbox.module.exports,
    };
  } catch (e) {
    throw new Error(`Failed to load CJS module "${filePath}": ${e.message}`);
  }
}

// ── Sandbox creation ──────────────────────────────────────

function createSandbox(filePath) {
  const moduleDir = path.dirname(filePath);

  return {
    module: { exports: {} },
    exports: {},
    require: (specifier) => {
      // Synchronous require for CJS interop
      const resolved = resolver.resolve(specifier, filePath);
      if (resolved.type === 'builtin') {
        return require(resolved.path);
      }
      // For file/package, we need to load synchronously
      const content = fs.readFileSync(resolved.path, 'utf-8');
      const subSandbox = createSandbox(resolved.path);
      const script = new vm.Script(content, { filename: resolved.path });
      const context = vm.createContext(subSandbox);
      script.runInContext(context);
      return subSandbox.module.exports;
    },
    __filename: filePath,
    __dirname: moduleDir,
    console,
    process: { ...process, cwd: () => moduleDir },
    Buffer,
    setTimeout,
    setInterval,
    clearTimeout,
    clearInterval,
    URL,
    URLSearchParams,
    TextEncoder,
    TextDecoder,
    // Mozhi bridge
    __mz_bridge: {
      mzToJs: value.mzToJs,
      jsToMz: value.jsToMz,
    },
  };
}

// ── ESM transformation ────────────────────────────────────

function transformESM(content, filePath) {
  let transformed = content;

  // Transform: import { a, b } from "./module.js"
  transformed = transformed.replace(
    /import\s*\{([^}]+)\}\s*from\s*["']([^"']+)["']\s*;?/g,
    (match, names, source) => {
      const resolved = resolver.resolve(source, filePath);
      const varName = `__import_${sanitize(source)}`;
      const namesList = names.split(',').map(s => s.trim());

      let code = `const ${varName} = require('${resolved.path}');\n`;
      for (const name of namesList) {
        const parts = name.split(/\s+as\s+/);
        const imported = parts[0].trim();
        const local = (parts[1] || parts[0]).trim();
        code += `const ${local} = ${varName}['${imported}'];\n`;
      }
      return code;
    }
  );

  // Transform: import * as name from "./module.js"
  transformed = transformed.replace(
    /import\s*\*\s*as\s+(\w+)\s+from\s*["']([^"']+)["']\s*;?/g,
    (match, name, source) => {
      const resolved = resolver.resolve(source, filePath);
      return `const ${name} = require('${resolved.path}');\n`;
    }
  );

  // Transform: import name from "./module.js" (default import)
  transformed = transformed.replace(
    /import\s+(\w+)\s+from\s*["']([^"']+)["']\s*;?/g,
    (match, name, source) => {
      const resolved = resolver.resolve(source, filePath);
      return `const ${name} = require('${resolved.path}');\n`;
    }
  );

  // Transform: export function name(...) { ... }  AND  export async function name(...) { ... }
  transformed = transformed.replace(
    /export\s+(async\s+)?function\s+(\w+)\s*\(([^)]*)\)\s*\{/g,
    (match, asyncKw, name, params) => {
      return `${asyncKw || ''}function ${name}(${params}) {`;
    }
  );

  // Find all function names that were exported
  const exportedFns = [];
  const origContent = content;
  const exportFnRegex = /export\s+(?:async\s+)?function\s+(\w+)/g;
  let m;
  while ((m = exportFnRegex.exec(origContent)) !== null) {
    exportedFns.push(m[1]);
  }

  // Transform: export const/let/var name = ...
  const exportedVars = [];
  const exportVarRegex = /export\s+(?:const|let|var)\s+(\w+)/g;
  while ((m = exportVarRegex.exec(origContent)) !== null) {
    exportedVars.push(m[1]);
  }
  transformed = transformed.replace(/export\s+(const|let|var)\s+/g, '$1 ');

  // Transform: export { a, b, c }
  const exportedNames = [];
  transformed = transformed.replace(
    /export\s*\{([^}]+)\}\s*;?/g,
    (match, names) => {
      const namesList = names.split(',').map(s => s.trim());
      for (const n of namesList) {
        const parts = n.split(/\s+as\s+/);
        const local = parts[0].trim();
        const exported = (parts[1] || parts[0]).trim();
        exportedNames.push({ local, exported });
      }
      return `/* re-export removed */`;
    }
  );

  // Transform: export default X
  transformed = transformed.replace(
    /export\s+default\s+/g,
    'module.exports.default = '
  );

  // Append all exports at the end
  const allExports = [];
  for (const fn of exportedFns) {
    allExports.push(`module.exports['${fn}'] = ${fn};`);
  }
  for (const v of exportedVars) {
    allExports.push(`module.exports['${v}'] = ${v};`);
  }
  for (const { local, exported } of exportedNames) {
    allExports.push(`module.exports['${exported}'] = ${local};`);
  }

  if (allExports.length > 0) {
    transformed += '\n' + allExports.join('\n') + '\n';
  }

  return transformed;
}

// ── Helpers ───────────────────────────────────────────────

function flattenExports(mod) {
  if (mod === null || mod === undefined) return {};
  if (typeof mod !== 'object') return { default: mod };

  const result = {};
  for (const key of Object.keys(mod)) {
    result[key] = mod[key];
  }
  if (mod.default !== undefined) {
    result.default = mod.default;
  }
  return result;
}

function isESM(content) {
  return /\bimport\s/.test(content) || /\bexport\s/.test(content);
}

function sanitize(str) {
  return str.replace(/[^a-zA-Z0-9]/g, '_');
}

function clearCache() {
  moduleCache.clear();
}

module.exports = { load, clearCache };
