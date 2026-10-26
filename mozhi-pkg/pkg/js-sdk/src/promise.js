// promise.js — JavaScript Promise ↔ Mozhi Future bridge
// Handles async interop between JS promises and Mozhi async values

const value = require('./value');
const handles = require('./handles');

// Track pending futures for Mozhi runtime
const pendingFutures = new Map(); // id → { resolve, reject, promise }
let nextFutureId = 1;

// ── JS Promise → Mozhi Future ────────────────────────────

function promiseToFuture(jsPromise) {
  const futureId = nextFutureId++;

  const future = {
    __mz_type: 'future',
    __future_id: futureId,
    state: 'pending', // pending | resolved | rejected
    value: null,
    error: null,
  };

  jsPromise.then(
    (result) => {
      future.state = 'resolved';
      future.value = value.jsToMz(result);
      if (pendingFutures.has(futureId)) {
        pendingFutures.get(futureId).resolve(future.value);
      }
    },
    (error) => {
      future.state = 'rejected';
      future.error = error instanceof Error
        ? { __mz_type: 'error', message: error.message, name: error.name, stack: error.stack }
        : value.jsToMz(error);
      if (pendingFutures.has(futureId)) {
        pendingFutures.get(futureId).reject(future.error);
      }
    }
  );

  pendingFutures.set(futureId, { future });
  return future;
}

// ── Mozhi Future await ────────────────────────────────────

function awaitFuture(future) {
  if (!future || future.__mz_type !== 'future') {
    return Promise.resolve(future);
  }

  if (future.state === 'resolved') {
    return Promise.resolve(future.value);
  }

  if (future.state === 'rejected') {
    return Promise.reject(future.error);
  }

  // Still pending — create a JS promise that resolves when future does
  return new Promise((resolve, reject) => {
    pendingFutures.set(future.__future_id, { resolve, reject, future });
  });
}

// ── Mozhi callback → JS Promise ───────────────────────────

function mzCallbackToPromise(mzFn) {
  return new Promise((resolve, reject) => {
    try {
      const wrapper = (err, result) => {
        if (err) reject(err);
        else resolve(result);
      };
      mzFn(wrapper);
    } catch (e) {
      reject(e);
    }
  });
}

// ── Check if value is a future ────────────────────────────

function isFuture(value) {
  return value && value.__mz_type === 'future';
}

// ── Cleanup ───────────────────────────────────────────────

function cleanupFuture(futureId) {
  pendingFutures.delete(futureId);
}

function stats() {
  return {
    pendingFutures: pendingFutures.size,
    nextFutureId,
  };
}

module.exports = {
  promiseToFuture,
  awaitFuture,
  mzCallbackToPromise,
  isFuture,
  cleanupFuture,
  stats,
};
