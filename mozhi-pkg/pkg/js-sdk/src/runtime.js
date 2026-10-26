// runtime.js — Complete JS runtime for Mozhi
// Initializes all interop subsystems and provides the main API

const bridge = require('./bridge');
const loader = require('./loader');
const resolver = require('./resolver');
const value = require('./value');
const handles = require('./handles');
const promise = require('./promise');
const callback = require('./callback');

class MozhiJsRuntime {
  constructor(options = {}) {
    this.basePath = options.basePath || process.cwd();
    this.debug = options.debug || false;
    this._modules = new Map();
  }

  // ── Import operations (for Mozhi compiler) ──────────────

  // import js { add } from "./math.js"
  async importNamed(specifier, names) {
    const mod = await loader.load(specifier, this.basePath);
    const result = {};
    for (const name of names) {
      let original, alias;
      if (name.includes(' as ')) {
        const parts = name.split(/\s+as\s+/);
        original = parts[0].trim();
        alias = parts[1].trim();
      } else {
        original = name;
        alias = name;
      }

      const val = mod.exports[original];
      if (val === undefined) {
        const available = Object.keys(mod.exports).join(', ');
        throw new Error(
          `Mozhi JS Import Error\n\n` +
          `Module "${specifier}" does not export "${original}".\n\n` +
          `Available exports:\n  ${available || '(none)'}`
        );
      }
      result[alias] = wrapExportedValue(val);
    }
    return result;
  }

  // import js * as math from "./math.js"
  async importNamespace(specifier) {
    const mod = await loader.load(specifier, this.basePath);
    const ns = {};
    for (const [key, value_] of Object.entries(mod.exports)) {
      ns[key] = wrapExportedValue(value_);
    }
    if (mod.default !== undefined) {
      ns.default = wrapExportedValue(mod.default);
    }
    return ns;
  }

  // import js express from "express"  (default import)
  async importDefault(specifier) {
    const mod = await loader.load(specifier, this.basePath);
    const defaultVal = mod.default || mod.exports;
    return wrapExportedValue(defaultVal);
  }

  // ── Call operations ─────────────────────────────────────

  call(fn, ...args) {
    return bridge.mz_js_call(
      typeof fn === 'object' && fn.__mz_handle ? fn.__mz_handle : handles.create(fn),
      ...args
    );
  }

  methodCall(obj, methodName, ...args) {
    return bridge.mz_js_method(
      typeof obj === 'object' && obj.__mz_handle ? obj.__mz_handle : handles.create(obj),
      methodName,
      ...args
    );
  }

  // ── Property operations ─────────────────────────────────

  get(obj, property) {
    return bridge.mz_js_get(
      typeof obj === 'object' && obj.__mz_handle ? obj.__mz_handle : handles.create(obj),
      property
    );
  }

  set(obj, property, value_) {
    bridge.mz_js_set(
      typeof obj === 'object' && obj.__mz_handle ? obj.__mz_handle : handles.create(obj),
      property,
      value_
    );
  }

  // ── Async operations ────────────────────────────────────

  async await(future) {
    return bridge.mz_js_await(
      typeof future === 'object' && future.__mz_handle
        ? future.__mz_handle
        : handles.create(future)
    );
  }

  // ── Callback creation ───────────────────────────────────

  callback(mzFn, options) {
    return callback.create(mzFn, options);
  }

  // ── Value conversion ────────────────────────────────────

  toJs(mzValue) { return value.mzToJs(mzValue); }
  toMz(jsValue) { return value.jsToMz(jsValue); }

  // ── Handle management ───────────────────────────────────

  createHandle(jsValue) { return handles.create(jsValue); }
  releaseHandle(handleId) { handles.release(handleId); }

  // ── Direct bridge operations ────────────────────────────

  mz_js_export(moduleHandleId, exportName) {
    return bridge.mz_js_export(moduleHandleId, exportName);
  }

  mz_js_call(fnHandleId, ...args) {
    return bridge.mz_js_call(fnHandleId, ...args);
  }

  // ── Cleanup ─────────────────────────────────────────────

  dispose() {
    handles.releaseAll();
    callback.releaseAll();
    loader.clearCache();
    resolver.clearCache();
    this._modules.clear();
  }

  // ── Debug info ──────────────────────────────────────────

  debugInfo() {
    return {
      handles: handles.stats(),
      callbacks: callback.stats(),
      futures: promise.stats(),
      modules: this._modules.size,
    };
  }
}

// Wrap an exported JS value for Mozhi consumption
// Functions become callable wrappers, objects become handle refs
function wrapExportedValue(val) {
  if (val === null || val === undefined) return null;
  if (typeof val === 'function') {
    // Return a callable wrapper that bridges Mozhi ↔ JS
    return function (...args) {
      const jsArgs = args.map(value.mzToJs);
      const result = val(...jsArgs);
      if (result instanceof Promise) {
        return promise.promiseToFuture(result);
      }
      return value.jsToMz(result);
    };
  }
  if (typeof val === 'object') {
    // Create a proxy that allows property access and method calls
    const handleId = handles.create(val);
    const jsObj = val; // capture in closure
    return new Proxy({}, {
      get(target, prop) {
        if (prop === '__mz_handle') return handleId;
        const propVal = jsObj[prop];
        if (typeof propVal === 'function') {
          return function (...args) {
            const jsArgs = args.map(value.mzToJs);
            const result = propVal.apply(jsObj, jsArgs);
            if (result instanceof Promise) {
              return promise.promiseToFuture(result);
            }
            return value.jsToMz(result);
          };
        }
        return value.jsToMz(propVal);
      },
      set(target, prop, value_) {
        jsObj[prop] = value.mzToJs(value_);
        return true;
      },
    });
  }
  return value.jsToMz(val);
}

module.exports = { MozhiJsRuntime, wrapExportedValue };
