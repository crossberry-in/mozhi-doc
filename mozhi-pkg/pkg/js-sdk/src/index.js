// index.js — @mozhi/js-sdk entry point
// Full JavaScript/NPM interoperability for Mozhi

const { MozhiJsRuntime } = require('./runtime');
const bridge = require('./bridge');
const loader = require('./loader');
const resolver = require('./resolver');
const value = require('./value');
const handles = require('./handles');
const promise = require('./promise');
const callback = require('./callback');

// ── Runtime API (all operations) ──────────────────────────

module.exports = {
  // Runtime class
  MozhiJsRuntime,

  // Bridge operations (direct access)
  mz_js_load: bridge.mz_js_load,
  mz_js_export: bridge.mz_js_export,
  mz_js_call: bridge.mz_js_call,
  mz_js_method: bridge.mz_js_method,
  mz_js_get: bridge.mz_js_get,
  mz_js_set: bridge.mz_js_set,
  mz_js_await: bridge.mz_js_await,
  mz_js_callback: bridge.mz_js_callback,
  mz_js_handle_create: bridge.mz_js_handle_create,
  mz_js_handle_release: bridge.mz_js_handle_release,

  // Value conversion
  mzToJs: value.mzToJs,
  jsToMz: value.jsToMz,
  mz_from_js: value.jsToMz,
  mz_value_to_js: value.mzToJs,

  // Module resolution
  resolve: resolver.resolve,

  // Module loading
  load: loader.load,

  // Sub-modules
  handles,
  promise,
  callback,

  // Version
  version: '1.0.0',
};
