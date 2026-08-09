// value.js — Mozhi ↔ JavaScript value conversion
// Handles automatic type mapping between the two runtimes

const handles = require('./handles');

// ── Mozhi → JavaScript ────────────────────────────────────

function mzToJs(value) {
  if (value === null || value === undefined) return null;

  switch (typeof value) {
    case 'number':
      return Number.isInteger(value) ? value : value; // Mozhi int→JS number, float→JS number
    case 'string':
      return value;
    case 'boolean':
      return value;

    case 'object':
      // Mozhi array → JS Array
      if (Array.isArray(value)) {
        return value.map(mzToJs);
      }

      // Mozhi map → JS Object
      if (value instanceof Map) {
        const obj = {};
        for (const [k, v] of value) {
          obj[String(k)] = mzToJs(v);
        }
        return obj;
      }

      // Mozhi ByteBuffer → Uint8Array (zero-copy if possible)
      if (value instanceof ArrayBuffer) {
        return new Uint8Array(value);
      }
      if (Buffer.isBuffer(value)) {
        return new Uint8Array(value.buffer, value.byteOffset, value.byteLength);
      }

      // Mozhi function → JS callable wrapper
      if (typeof value === 'function') {
        return (...args) => {
          const jsArgs = args.map(jsToMz);
          const result = value(...jsArgs);
          return mzToJs(result);
        };
      }

      // Mozhi handle reference → JS value
      if (value.__mz_handle !== undefined) {
        return handles.get(value.__mz_handle);
      }

      // Generic object → plain JS object
      const obj = {};
      for (const key of Object.keys(value)) {
        obj[key] = mzToJs(value[key]);
      }
      return obj;

    default:
      return value;
  }
}

// ── JavaScript → Mozhi ────────────────────────────────────

function jsToMz(value) {
  if (value === null || value === undefined) return null;

  switch (typeof value) {
    case 'number':
      return value; // JS number → Mozhi number (int or float)
    case 'string':
      return value;
    case 'boolean':
      return value;

    case 'object':
      // JS Array → Mozhi array
      if (Array.isArray(value)) {
        return value.map(jsToMz);
      }

      // JS Buffer/Uint8Array → Mozhi buffer
      if (Buffer.isBuffer(value)) {
        return value;
      }
      if (value instanceof Uint8Array) {
        return Buffer.from(value.buffer, value.byteOffset, value.byteLength);
      }
      if (value instanceof ArrayBuffer) {
        return Buffer.from(value);
      }

      // JS Promise → Mozhi Future (handled by promise.js)
      if (value instanceof Promise) {
        return value; // Pass through, promise.js handles wrapping
      }

      // JS Date → Mozhi datetime
      if (value instanceof Date) {
        return {
          __mz_type: 'datetime',
          timestamp: value.getTime(),
          iso: value.toISOString(),
        };
      }

      // JS Error → Mozhi error
      if (value instanceof Error) {
        return {
          __mz_type: 'error',
          message: value.message,
          name: value.name,
          stack: value.stack,
          cause: value.cause ? jsToMz(value.cause) : null,
        };
      }

      // JS Map → Mozhi map
      if (value instanceof Map) {
        const mzMap = new Map();
        for (const [k, v] of value) {
          mzMap.set(jsToMz(k), jsToMz(v));
        }
        return mzMap;
      }

      // JS Set → Mozhi array
      if (value instanceof Set) {
        return Array.from(value).map(jsToMz);
      }

      // JS function → Mozhi callable (via handle)
      if (typeof value === 'function') {
        const fnHandleId = handles.create(value);
        return { __mz_handle: fnHandleId };
      }

      // JS object → Mozhi object (via handle for identity)
      const objHandleId = handles.create(value);
      return { __mz_handle: objHandleId };

    case 'function':
      const handleId = handles.create(value);
      return { __mz_handle: handleId };

    case 'bigint':
      return Number(value); // Mozhi doesn't have bigint, convert to number

    case 'symbol':
      return value.toString(); // Convert symbol to string

    default:
      return value;
  }
}

// ── Bidirectional wrapper ─────────────────────────────────

function wrapJsFunction(fn) {
  return function (...args) {
    const mzArgs = args.map(jsToMz);
    const result = fn(...mzArgs);
    return mzToJs(result);
  };
}

function wrapMzFunction(fn) {
  return function (...args) {
    const jsArgs = args.map(mzToJs);
    const result = fn(...jsArgs);
    return jsToMz(result);
  };
}

// ── Type checking helpers ─────────────────────────────────

function isMzValue(value) {
  if (value === null || value === undefined) return true;
  const t = typeof value;
  if (t === 'number' || t === 'string' || t === 'boolean') return true;
  if (Array.isArray(value)) return value.every(isMzValue);
  if (value instanceof Map) return true;
  if (value.__mz_handle !== undefined) return true;
  if (value.__mz_type) return true;
  return false;
}

function isJsValue(value) {
  if (value === null || value === undefined) return true;
  const t = typeof value;
  if (t === 'number' || t === 'string' || t === 'boolean') return true;
  if (Array.isArray(value)) return true;
  if (Buffer.isBuffer(value)) return true;
  if (value instanceof Uint8Array) return true;
  if (value instanceof Promise) return true;
  if (value instanceof Date) return true;
  if (value instanceof Error) return true;
  if (t === 'function') return true;
  if (t === 'object') return true;
  return false;
}

module.exports = {
  mzToJs,
  jsToMz,
  wrapJsFunction,
  wrapMzFunction,
  isMzValue,
  isJsValue,
};
