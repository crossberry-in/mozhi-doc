// test runner for js-sdk
const path = require('path');
const sdk = require('../src/index');

let passed = 0;
let failed = 0;
const errors = [];

function assert(condition, message) {
  if (condition) {
    passed++;
  } else {
    failed++;
    errors.push(message);
    console.log(`  ✗ FAIL: ${message}`);
  }
}

function assertEq(actual, expected, message) {
  if (actual === expected) {
    passed++;
  } else {
    failed++;
    errors.push(`${message}: expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
    console.log(`  ✗ FAIL: ${message} — expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
  }
}

async function run() {
  console.log('╔════════════════════════════════════════╗');
  console.log('║  @mozhi/js-sdk — Test Suite           ║');
  console.log('╚════════════════════════════════════════╝');
  console.log('');

  const rt = new sdk.MozhiJsRuntime({
    basePath: path.join(__dirname, 'jsinterop'),
  });

  // ── Test 1: Named import ──────────────────────────────
  console.log('── Test: Named Import ──');
  {
    const mod = await rt.importNamed('./fixtures/math.js', ['add', 'multiply', 'PI']);
    assertEq(mod.add(10, 20), 30, 'add(10, 20) === 30');
    assertEq(mod.multiply(5, 6), 30, 'multiply(5, 6) === 30');
    assertEq(Math.abs(mod.PI - 3.14159265358979) < 0.0001, true, 'PI ≈ 3.14159');
  }
  console.log('');

  // ── Test 2: Default import ────────────────────────────
  console.log('── Test: Default Import ──');
  {
    const defaultMod = await rt.importDefault('./fixtures/cjs_module.js');
    assert(typeof defaultMod === 'object', 'default import is object');
    assertEq(defaultMod.greet('World'), 'Hello, World!', 'greet("World")');
    assertEq(defaultMod.add(3, 4), 7, 'add(3, 4) === 7');
    assertEq(defaultMod.version, '1.0.0', 'version === "1.0.0"');
  }
  console.log('');

  // ── Test 3: Namespace import ──────────────────────────
  console.log('── Test: Namespace Import ──');
  {
    const ns = await rt.importNamespace('./fixtures/math.js');
    assert(typeof ns.add === 'function', 'namespace has add function');
    assert(typeof ns.multiply === 'function', 'namespace has multiply function');
    assertEq(ns.square(9), 81, 'square(9) === 81');
    assertEq(ns.subtract(10, 3), 7, 'subtract(10, 3) === 7');
  }
  console.log('');

  // ── Test 4: Alias import ──────────────────────────────
  console.log('── Test: Alias Import ──');
  {
    const mod = await rt.importNamed('./fixtures/math.js', ['add as sum', 'multiply as mul']);
    assert(typeof mod.sum === 'function', 'alias sum exists');
    assert(typeof mod.mul === 'function', 'alias mul exists');
    assertEq(mod.sum(10, 20), 30, 'sum(10, 20) === 30');
    assertEq(mod.mul(5, 6), 30, 'mul(5, 6) === 30');
  }
  console.log('');

  // ── Test 5: CommonJS module ───────────────────────────
  console.log('── Test: CommonJS Module ──');
  {
    const cjs = await rt.importDefault('./fixtures/cjs_module.js');
    assertEq(cjs.greet('Mozhi'), 'Hello, Mozhi!', 'CJS greet');
    assertEq(cjs.add(100, 200), 300, 'CJS add');
  }
  console.log('');

  // ── Test 6: Async/Promise ─────────────────────────────
  console.log('── Test: Async/Promise ──');
  {
    const mod = await rt.importNamed('./fixtures/async_module.js', ['fetchData', 'delayedAdd']);

    const data = await rt.await(mod.fetchData('http://example.com'));
    assert(typeof data === 'object', 'fetchData returns object');
    assertEq(data.url, 'http://example.com', 'fetchData url preserved');

    const sum = await rt.await(mod.delayedAdd(10, 20));
    assertEq(sum, 30, 'delayedAdd(10, 20) === 30');
  }
  console.log('');

  // ── Test 7: Object method with `this` ─────────────────
  console.log('── Test: Method Call (this binding) ──');
  {
    const mod = await rt.importNamed('./fixtures/async_module.js', ['createCounter']);
    const counter = mod.createCounter();
    assert(typeof counter === 'object', 'createCounter returns object');

    // Test method calls with this binding
    const inc1 = rt.methodCall(counter, 'increment');
    const inc2 = rt.methodCall(counter, 'increment');
    const inc3 = rt.methodCall(counter, 'increment');
    assertEq(inc3, 3, 'counter.increment() x3 === 3');

    const dec = rt.methodCall(counter, 'decrement');
    assertEq(dec, 2, 'counter.decrement() === 2');

    const val = rt.methodCall(counter, 'get');
    assertEq(val, 2, 'counter.get() === 2');
  }
  console.log('');

  // ── Test 8: Callback ──────────────────────────────────
  console.log('── Test: Callback ──');
  {
    let callbackCalled = false;
    let callbackResult = null;

    const cb = rt.callback((result) => {
      callbackCalled = true;
      callbackResult = result;
    });

    assert(typeof cb === 'function', 'callback is a JS function');

    // Call the callback
    cb(42);
    assert(callbackCalled, 'callback was called');
    assertEq(callbackResult, 42, 'callback received correct value');
  }
  console.log('');

  // ── Test 9: Value conversion ──────────────────────────
  console.log('── Test: Value Conversion ──');
  {
    // JS → Mozhi
    assertEq(sdk.jsToMz(42), 42, 'number passthrough');
    assertEq(sdk.jsToMz('hello'), 'hello', 'string passthrough');
    assertEq(sdk.jsToMz(true), true, 'boolean passthrough');
    assertEq(sdk.jsToMz(null), null, 'null passthrough');

    const arr = sdk.jsToMz([1, 2, 3]);
    assert(Array.isArray(arr), 'array converted');
    assertEq(arr.length, 3, 'array length');

    // Mozhi → JS
    assertEq(sdk.mzToJs(42), 42, 'mz number to JS');
    assertEq(sdk.mzToJs('test'), 'test', 'mz string to JS');

    // Buffer conversion
    const buf = Buffer.from([1, 2, 3, 4]);
    const uint8 = sdk.jsToMz(buf);
    assert(uint8 instanceof Uint8Array, 'Buffer → Uint8Array');
  }
  console.log('');

  // ── Test 10: Error handling ───────────────────────────
  console.log('── Test: Error Handling ──');
  {
    try {
      rt.mz_js_export(999, 'nonexistent');
      assert(false, 'should throw on invalid handle');
    } catch (e) {
      assert(e.message.includes('Invalid handle'), 'error message for invalid handle');
    }

    try {
      await rt.importNamed('./fixtures/math.js', ['nonexistent_function']);
      assert(false, 'should throw on missing export');
    } catch (e) {
      assert(e.message.includes('does not export'), 'error for missing export');
    }
  }
  console.log('');

  // ── Test 11: Module caching ───────────────────────────
  console.log('── Test: Module Caching ──');
  {
    const mod1 = await rt.importNamed('./fixtures/math.js', ['add']);
    const mod2 = await rt.importNamed('./fixtures/math.js', ['add']);
    // Both should reference the same underlying module
    assertEq(mod1.add(1, 2), 3, 'cached module works (call 1)');
    assertEq(mod2.add(3, 4), 7, 'cached module works (call 2)');
  }
  console.log('');

  // ── Test 12: Handle lifecycle ─────────────────────────
  console.log('── Test: Handle Lifecycle ──');
  {
    const obj = { x: 1, y: 2 };
    const handleId = sdk.handles.create(obj);
    assert(typeof handleId === 'number', 'handle ID is number');

    const retrieved = sdk.handles.get(handleId);
    assertEq(retrieved.x, 1, 'handle retrieves correct object');

    sdk.handles.retain(handleId);
    sdk.handles.release(handleId);
    const still = sdk.handles.get(handleId);
    assertEq(still.x, 1, 'object survives after retain+release');

    sdk.handles.release(handleId);
    try {
      sdk.handles.get(handleId);
      assert(false, 'should throw after all releases');
    } catch (e) {
      assert(e.message.includes('Invalid handle'), 'released handle throws');
    }
  }
  console.log('');

  // ── Report ────────────────────────────────────────────
  console.log('════════════════════════════════════════');
  console.log(`  Passed: ${passed}`);
  console.log(`  Failed: ${failed}`);
  if (errors.length > 0) {
    console.log('');
    console.log('  Failures:');
    for (const err of errors) {
      console.log(`    • ${err}`);
    }
  }
  console.log('════════════════════════════════════════');

  // Cleanup
  rt.dispose();

  process.exit(failed > 0 ? 1 : 0);
}

run().catch(e => {
  console.error('Test runner error:', e);
  process.exit(1);
});
