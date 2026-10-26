// handles.js — JS object handle/lifetime management for Mozhi
// Prevents premature GC of JS objects still referenced by Mozhi

let nextHandleId = 1;
const handles = new Map(); // id -> { value, refCount, createdAt }
const valueToHandle = new WeakMap(); // value -> id (for identity preservation)

function create(value) {
  // Check if we already have a handle for this value
  if (value !== null && typeof value === 'object') {
    const existingId = valueToHandle.get(value);
    if (existingId !== undefined) {
      retain(existingId);
      return existingId;
    }
  }

  const id = nextHandleId++;
  handles.set(id, {
    value,
    refCount: 1,
    createdAt: Date.now(),
  });

  if (value !== null && typeof value === 'object') {
    valueToHandle.set(value, id);
  }

  return id;
}

function retain(handleId) {
  const handle = handles.get(handleId);
  if (handle) {
    handle.refCount++;
  }
  return handleId;
}

function release(handleId) {
  const handle = handles.get(handleId);
  if (!handle) return;

  handle.refCount--;
  if (handle.refCount <= 0) {
    if (handle.value !== null && typeof handle.value === 'object') {
      valueToHandle.delete(handle.value);
    }
    handles.delete(handleId);
  }
}

function get(handleId) {
  const handle = handles.get(handleId);
  if (!handle) {
    throw new Error(`Mozhi JS Handle Error: Invalid handle ${handleId}`);
  }
  return handle.value;
}

function set(handleId, value) {
  const handle = handles.get(handleId);
  if (!handle) {
    throw new Error(`Mozhi JS Handle Error: Invalid handle ${handleId}`);
  }
  handle.value = value;
}

function inspect(handleId) {
  const handle = handles.get(handleId);
  if (!handle) return null;
  return {
    id: handleId,
    type: typeof handle.value,
    constructor: handle.value?.constructor?.name || 'null',
    refCount: handle.refCount,
    createdAt: handle.createdAt,
  };
}

function stats() {
  return {
    totalHandles: handles.size,
    nextId: nextHandleId,
  };
}

function releaseAll() {
  handles.clear();
  nextHandleId = 1;
}

module.exports = { create, retain, release, get, set, inspect, stats, releaseAll };
