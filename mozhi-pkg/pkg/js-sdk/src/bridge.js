// bridge.js — Main Mozhi ↔ JavaScript runtime bridge
// Provides all interop operations: load, call, get, set, await, callback

const loader = require('./loader');
const value = require('./value');
const handles = require('./handles');
const promise = require('./promise');
const callback = require('./callback');

// ── Module operations ─────────────────────────────────────

// mz_js_load(specifier, fromPath) → moduleId (handle)
async function mz_js_load(specifier, fromPath) {
  const mod = await loader.load(specifier, fromPath);
  return handles.create(mod);
}

// mz_js_export(moduleHandle, exportName) → value or handle
function mz_js_export(moduleHandleId, exportName) {
  const mod = handles.get(moduleHandleId);
  if (!mod || !mod.exports) {
    throw new Error(`Module handle ${moduleHandleId} has no exports`);
  }

  if (exportName === 'default') {
    return value.jsToMz(mod.default || mod.exports);
  }

  const value_ = mod.exports[exportName];
  if (value_ === undefined) {
    // List available exports for error message
    const available = Object.keys(mod.exports).join(', ');
    throw new Error(
      `Mozhi JS Import Error\n\n` +
      `Module does not export "${exportName}".\n\n` +
      `Available exports:\n  ${available || '(none)'}`
    );
  }

  return value.jsToMz(value_);
}

// ── Call operations ───────────────────────────────────────

// mz_js_call(fnHandle, ...args) → result
function mz_js_call(fnHandleId, ...args) {
  const fn = handles.get(fnHandleId);
  if (typeof fn !== 'function') {
    throw new Error(`Handle ${fnHandleId} is not a function`);
  }

  const jsArgs = args.map(value.mzToJs);

  try {
    const result = fn(...jsArgs);
    return value.jsToMz(result);
  } catch (e) {
    throw convertJsError(e);
  }
}

// mz_js_method(objHandle, methodName, ...args) → result
// Preserves `this` context
function mz_js_method(objHandleId, methodName, ...args) {
  const obj = handles.get(objHandleId);
  if (obj === null || obj === undefined) {
    throw new Error(`Cannot call method on null/undefined`);
  }

  const method = obj[methodName];
  if (typeof method !== 'function') {
    throw new Error(`"${methodName}" is not a method on object`);
  }

  const jsArgs = args.map(value.mzToJs);

  try {
    // Call with `this` bound to the object
    const result = method.apply(obj, jsArgs);
    return value.jsToMz(result);
  } catch (e) {
    throw convertJsError(e);
  }
}

// ── Property operations ───────────────────────────────────

// mz_js_get(objHandle, property) → value
function mz_js_get(objHandleId, property) {
  const obj = handles.get(objHandleId);
  if (obj === null || obj === undefined) {
    throw new Error(`Cannot access property on null/undefined`);
  }

  const value_ = obj[property];
  return value.jsToMz(value_);
}

// mz_js_set(objHandle, property, value) → void
function mz_js_set(objHandleId, property, mzValue) {
  const obj = handles.get(objHandleId);
  if (obj === null || obj === undefined) {
    throw new Error(`Cannot set property on null/undefined`);
  }

  obj[property] = value.mzToJs(mzValue);
}

// ── Async operations ──────────────────────────────────────

// mz_js_await(futureHandle) → resolved value
async function mz_js_await(futureHandleId) {
  const promise_ = handles.get(futureHandleId);
  if (!(promise_ instanceof Promise)) {
    // Not a promise, just return the value
    return promise_;
  }

  try {
    const result = await promise_;
    return value.jsToMz(result);
  } catch (e) {
    throw convertJsError(e);
  }
}

// ── Callback operations ───────────────────────────────────

// mz_js_callback(mzFn) → JS function wrapper
function mz_js_callback(mzFn) {
  return callback.create(mzFn);
}

// ── Handle operations ─────────────────────────────────────

function mz_js_handle_create(jsValue) {
  return handles.create(value.mzToJs(jsValue));
}

function mz_js_handle_release(handleId) {
  handles.release(handleId);
}

// ── Error conversion ──────────────────────────────────────

function convertJsError(jsError) {
  if (jsError instanceof Error) {
    const mzError = {
      __mz_type: 'error',
      message: jsError.message,
      name: jsError.name || 'Error',
      stack: jsError.stack || '',
      cause: jsError.cause ? convertJsError(jsError.cause) : null,
    };
    return mzError;
  }
  return value.jsToMz(jsError);
}

// ── Convenience: one-shot import + call ───────────────────

async function importAndCall(specifier, exportName, args, fromPath) {
  const modHandle = await mz_js_load(specifier, fromPath);
  const fn = mz_js_export(modHandle, exportName);

  if (typeof fn === 'object' && fn.__mz_handle) {
    return mz_js_call(fn.__mz_handle, ...args);
  }

  // Direct function call
  if (typeof fn === 'function') {
    const jsArgs = args.map(value.mzToJs);
    const result = fn(...jsArgs);
    return value.jsToMz(result);
  }

  return fn;
}

// ── Namespace object ──────────────────────────────────────

async function loadNamespace(specifier, fromPath) {
  const mod = await loader.load(specifier, fromPath);
  const ns = {};

  for (const [key, value_] of Object.entries(mod.exports)) {
    ns[key] = value.jsToMz(value_);
  }

  // Add default
  if (mod.default !== undefined) {
    ns.default = value.jsToMz(mod.default);
  }

  return ns;
}

module.exports = {
  // Module
  mz_js_load,
  mz_js_export,
  // Call
  mz_js_call,
  mz_js_method,
  // Property
  mz_js_get,
  mz_js_set,
  // Async
  mz_js_await,
  // Callback
  mz_js_callback,
  // Handles
  mz_js_handle_create,
  mz_js_handle_release,
  // Convenience
  importAndCall,
  loadNamespace,
  // Value conversion
  mzToJs: value.mzToJs,
  jsToMz: value.jsToMz,
};
