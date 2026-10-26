// callback.js — Mozhi function → JavaScript callback wrapper
// Creates JS-callable functions that invoke Mozhi functions

const value = require('./value');
const handles = require('./handles');

// Track active callbacks for lifetime management
const activeCallbacks = new Map(); // id → { mzFn, jsFn, createdAt }
let nextCallbackId = 1;

// ── Create JS callback from Mozhi function ────────────────

function create(mzFn, options = {}) {
  const callbackId = nextCallbackId++;
  const { once = false, context = null } = options;

  const jsFn = function (...args) {
    // Convert JS args to Mozhi values
    const mzArgs = args.map(value.jsToMz);

    try {
      let result;
      if (typeof mzFn === 'function') {
        result = mzFn(...mzArgs);
      } else if (mzFn && mzFn.__mz_handle) {
        // Mozhi function reference via handle
        const fn = handles.get(mzFn.__mz_handle);
        if (typeof fn === 'function') {
          result = fn(...mzArgs);
        } else {
          throw new Error(`Handle is not a callable function`);
        }
      } else {
        throw new Error(`Invalid Mozhi function reference`);
      }

      // Convert result back to JS
      const jsResult = value.mzToJs(result);

      // If once, auto-release
      if (once) {
        release(callbackId);
      }

      return jsResult;
    } catch (e) {
      // Convert Mozhi errors to JS errors
      if (e && e.__mz_type === 'error') {
        const jsError = new Error(e.message);
        jsError.name = e.name || 'MozhiError';
        jsError.stack = e.stack || '';
        throw jsError;
      }
      throw e;
    }
  };

  // Attach metadata
  jsFn.__callback_id = callbackId;
  jsFn.__is_mz_callback = true;

  activeCallbacks.set(callbackId, {
    mzFn,
    jsFn,
    createdAt: Date.now(),
    once,
    context,
  });

  return jsFn;
}

// ── Release callback ──────────────────────────────────────

function release(callbackId) {
  activeCallbacks.delete(callbackId);
}

// ── Release all callbacks ─────────────────────────────────

function releaseAll() {
  activeCallbacks.clear();
}

// ── Check if value is a Mozhi callback ────────────────────

function isCallback(value) {
  return value && value.__is_mz_callback === true;
}

// ── Stats ─────────────────────────────────────────────────

function stats() {
  return {
    activeCallbacks: activeCallbacks.size,
    nextCallbackId,
  };
}

// ── Wrap JS callback for Mozhi ────────────────────────────

function wrapJsCallback(jsFn) {
  return function (...args) {
    const jsArgs = args.map(value.mzToJs);
    const result = jsFn(...jsArgs);

    // If result is a Promise, wrap as Mozhi future
    if (result instanceof Promise) {
      const promise = require('./promise');
      return promise.promiseToFuture(result);
    }

    return value.jsToMz(result);
  };
}

module.exports = {
  create,
  release,
  releaseAll,
  isCallback,
  stats,
  wrapJsCallback,
};
