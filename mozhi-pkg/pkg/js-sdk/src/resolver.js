// resolver.js — Node.js-compatible module resolution for Mozhi
// Resolves: relative paths, node_modules, node: builtins, scoped packages
// No hardcoded package lists — uses Node's own resolution algorithm

const path = require('path');
const fs = require('fs');
const Module = require('module');

// Cache resolved paths
const resolveCache = new Map();

// ── Main resolver ─────────────────────────────────────────

function resolve(specifier, fromPath) {
  const cacheKey = `${fromPath}::${specifier}`;
  if (resolveCache.has(cacheKey)) {
    return resolveCache.get(cacheKey);
  }

  let resolved;

  // 1. node: builtins
  if (specifier.startsWith('node:')) {
    resolved = resolveBuiltin(specifier);
  }
  // 2. Relative paths
  else if (specifier.startsWith('./') || specifier.startsWith('../') || specifier.startsWith('/')) {
    resolved = resolveRelative(specifier, fromPath);
  }
  // 3. Package from node_modules
  else {
    resolved = resolvePackage(specifier, fromPath);
  }

  if (!resolved) {
    const searchPaths = getSearchPaths(fromPath);
    throw createResolveError(specifier, searchPaths);
  }

  resolveCache.set(cacheKey, resolved);
  return resolved;
}

// ── Node builtins ─────────────────────────────────────────

function resolveBuiltin(specifier) {
  const name = specifier.replace(/^node:/, '');
  const builtins = Module.builtinModules || [];

  if (builtins.includes(name)) {
    return { type: 'builtin', name, path: name };
  }

  // Subpath: node:fs/promises
  const parts = name.split('/');
  if (builtins.includes(parts[0])) {
    return { type: 'builtin', name, path: name };
  }

  return null;
}

// ── Relative resolution ───────────────────────────────────

function resolveRelative(specifier, fromPath) {
  // fromPath could be a file or directory - check first
  let baseDir;
  if (isDirectory(fromPath)) {
    baseDir = fromPath;
  } else {
    baseDir = path.dirname(fromPath);
  }
  const basePath = path.resolve(baseDir, specifier);

  // Try exact path
  if (tryFile(basePath)) return { type: 'file', path: basePath };

  // Try .js extension
  if (tryFile(basePath + '.js')) return { type: 'file', path: basePath + '.js' };

  // Try .mjs extension
  if (tryFile(basePath + '.mjs')) return { type: 'file', path: basePath + '.mjs' };

  // Try .cjs extension
  if (tryFile(basePath + '.cjs')) return { type: 'file', path: basePath + '.cjs' };

  // Try as directory with index
  if (tryDirectory(basePath)) return { type: 'file', path: findIndex(basePath) };

  return null;
}

// ── Package resolution from node_modules ──────────────────

function resolvePackage(specifier, fromPath) {
  // Parse package name and subpath
  let pkgName, subpath;
  if (specifier.startsWith('@')) {
    // Scoped: @scope/package or @scope/package/subpath
    const parts = specifier.split('/');
    pkgName = parts.slice(0, 2).join('/');
    subpath = parts.length > 2 ? './' + parts.slice(2).join('/') : '.';
  } else {
    const parts = specifier.split('/');
    pkgName = parts[0];
    subpath = parts.length > 1 ? './' + parts.slice(1).join('/') : '.';
  }

  // Walk up node_modules
  const searchPaths = getSearchPaths(fromPath);
  for (const searchDir of searchPaths) {
    const pkgDir = path.join(searchDir, 'node_modules', pkgName);
    if (!isDirectory(pkgDir)) continue;

    const pkgJsonPath = path.join(pkgDir, 'package.json');
    if (!tryFile(pkgJsonPath)) continue;

    // Read package.json
    let pkgJson;
    try {
      pkgJson = JSON.parse(fs.readFileSync(pkgJsonPath, 'utf-8'));
    } catch {
      continue;
    }

    // Resolve subpath using exports or main
    if (subpath === '.') {
      const resolved = resolvePackageEntry(pkgDir, pkgJson);
      if (resolved) return { type: 'package', name: pkgName, path: resolved, pkgDir };
    } else {
      // Subpath exports
      if (pkgJson.exports) {
        const resolved = resolveExports(pkgDir, pkgJson.exports, subpath);
        if (resolved) return { type: 'package', name: pkgName, path: resolved, pkgDir };
      }

      // Fallback: direct file
      const directPath = path.join(pkgDir, subpath);
      if (tryFile(directPath)) return { type: 'package', name: pkgName, path: directPath, pkgDir };
      if (tryFile(directPath + '.js')) return { type: 'package', name: pkgName, path: directPath + '.js', pkgDir };
    }
  }

  return null;
}

// ── Package entry resolution ──────────────────────────────

function resolvePackageEntry(pkgDir, pkgJson) {
  // 1. exports field (modern)
  if (pkgJson.exports) {
    const resolved = resolveExports(pkgDir, pkgJson.exports, '.');
    if (resolved) return resolved;
  }

  // 2. module field (ESM)
  if (pkgJson.module) {
    const p = path.join(pkgDir, pkgJson.module);
    if (tryFile(p)) return p;
  }

  // 3. main field (CJS)
  if (pkgJson.main) {
    const p = path.join(pkgDir, pkgJson.main);
    if (tryFile(p)) return p;
  }

  // 4. index.js fallback
  const indexPath = path.join(pkgDir, 'index.js');
  if (tryFile(indexPath)) return indexPath;

  return null;
}

// ── Exports field resolution ──────────────────────────────

function resolveExports(pkgDir, exports, subpath) {
  if (typeof exports === 'string') {
    if (subpath === '.') {
      const p = path.join(pkgDir, exports);
      return tryFile(p) ? p : null;
    }
    return null;
  }

  if (typeof exports !== 'object') return null;

  // Direct subpath map
  if (exports[subpath] !== undefined) {
    return resolveExportTarget(pkgDir, exports[subpath]);
  }

  // Conditional exports (import, require, default)
  if (subpath === '.' && (exports['.'] !== undefined)) {
    return resolveExportTarget(pkgDir, exports['.']);
  }

  // Pattern matching: "./*"
  for (const [pattern, target] of Object.entries(exports)) {
    if (pattern.includes('*')) {
      const regex = new RegExp('^' + pattern.replace('*', '(.*)') + '$');
      const match = subpath.match(regex);
      if (match) {
        const resolved = resolveExportTarget(pkgDir, target);
        if (resolved) return resolved.replace('*', match[1]);
      }
    }
  }

  return null;
}

function resolveExportTarget(pkgDir, target) {
  if (typeof target === 'string') {
    const p = path.join(pkgDir, target);
    return tryFile(p) ? p : null;
  }

  if (typeof target === 'object') {
    // Conditional: try import → require → default
    for (const condition of ['import', 'require', 'default', 'node']) {
      if (target[condition]) {
        const resolved = resolveExportTarget(pkgDir, target[condition]);
        if (resolved) return resolved;
      }
    }
  }

  return null;
}

// ── Search paths ──────────────────────────────────────────

function getSearchPaths(fromPath) {
  const paths = [];
  let dir = path.dirname(path.resolve(fromPath));

  while (true) {
    paths.push(dir);
    const parent = path.dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }

  return paths;
}

// ── File helpers ──────────────────────────────────────────

function tryFile(p) {
  try {
    return fs.statSync(p).isFile();
  } catch {
    return false;
  }
}

function tryDirectory(p) {
  try {
    return fs.statSync(p).isDirectory();
  } catch {
    return false;
  }
}

function isDirectory(p) {
  try {
    return fs.statSync(p).isDirectory();
  } catch {
    return false;
  }
}

function findIndex(dir) {
  for (const ext of ['.js', '.mjs', '.cjs', '']) {
    const p = path.join(dir, 'index' + ext);
    if (tryFile(p)) return p;
  }
  return null;
}

// ── Error creation ────────────────────────────────────────

function createResolveError(specifier, searchPaths) {
  const searched = searchPaths
    .map(p => `  ${path.join(p, 'node_modules', specifier)}`)
    .join('\n');

  const error = new Error(
    `Mozhi JS Import Error\n\n` +
    `Package: "${specifier}"\n\n` +
    `Could not resolve JavaScript module.\n\n` +
    `Searched:\n${searched}\n\n` +
    `Check:\n` +
    `  - package installation (npm install ${specifier.split('/')[0]})\n` +
    `  - package.json exports field\n` +
    `  - Node.js version compatibility`
  );
  error.code = 'MODULE_NOT_FOUND';
  error.specifier = specifier;
  return error;
}

// ── Clear cache ───────────────────────────────────────────

function clearCache() {
  resolveCache.clear();
}

module.exports = {
  resolve,
  resolveBuiltin,
  resolveRelative,
  resolvePackage,
  clearCache,
};
