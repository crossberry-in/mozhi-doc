// Async module fixture
export async function fetchData(url) {
  return { url, data: 'mock data', timestamp: Date.now() };
}

export async function delayedAdd(a, b) {
  await new Promise(r => setTimeout(r, 10));
  return a + b;
}

export function createCounter() {
  let count = 0;
  return {
    increment() { count++; return count; },
    decrement() { count--; return count; },
    get() { return count; },
  };
}
