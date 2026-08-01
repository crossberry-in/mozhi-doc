# Sino Performance Benchmark Report

**Benchmark Version:** 3.0.0  
**Date:** 2026-08-01 12:23:35  
**Sino Version:** Sino v1.0 (C Implementation)  
**Build Hash:** 817cc1b5c13547a5  
**Git Commit:** c16a659  
**Build Mode:** Release (-O3 -march=native)  
**Interpreter Hash:** 5065b8dd487010e9  
**Binary Size:** 54.7 KB  

## Environment

| Property | Value |
|----------|-------|
| OS | Linux 5.10.134-013.8.3.kangaroo.al8.x86_64 |
| Architecture | x86_64 |
| CPU Model | Intel(R) Xeon(R) Processor |
| CPU Frequency | 3200.0 MHz |
| CPU Cache | 516096 KB |
| Physical Cores | 2 |
| Logical Cores | 2 |
| RAM Total | 4041 MB |
| RAM Available | 3551 MB |
| Disk Type | unknown |
| Filesystem | 2% |
| Page Size | 4096 bytes |
| NUMA Nodes | 0 |
| Locale | unknown |
| Timezone | UTC |
| Runs per benchmark | 10 (warmup: 2) |

## Performance Scores

| Category | Score |
|----------|-------|
| Runtime | 65.4 / 100 |
| Collections | 82.4 / 100 |
| Strings | 68.4 / 100 |
| Math | 64.2 / 100 |
| Compiler | 100.0 / 100 |
| Error Handling | 100.0 / 100 |
| **Overall** | **76.9 / 100** |

---

## Detailed Results

### Core Runtime

| ID | Benchmark | Description | Mean (ms) | Median | P95 | P99 | Throughput (ops/s) | Mem (MB) | Status | Reason | Regression |
|----|----------|-------------|-----------|--------|-----|-----|---------------------|----------|--------|--------|------------|
| BR001 | startup_shutdown | Program startup and shutdown time (echo single value) | 0.44 | 0.43 | 0.47 | 0.47 | 2,290 | 18.2 | PASS | Mean 0.44 ms within threshold (100 ms) | +3.3% (stable) |
| BR002 | function_call | Function call overhead: 100,000 calls to add(a,b) | 55.95 | 55.41 | 58.88 | 60.81 | 1,787,374 | 18.2 | PASS | Mean 55.95 ms within threshold (500 ms) | +1.6% (stable) |
| BR003 | recursive_fibonacci | Recursive Fibonacci(25): tests function call + recursion | 95.80 | 95.72 | 96.46 | 96.75 | 2,534,200 | 18.2 | PASS | Mean 95.80 ms within threshold (5000 ms) | -0.2% (stable) |
| BR004 | nested_calls | Nested function calls (5 levels deep): 100,000 iterations | 150.23 | 149.83 | 152.55 | 153.69 | 665,648 | 18.2 | PASS | Mean 150.23 ms within threshold (500 ms) | +0.7% (stable) |
| BR005 | loop_sum | Simple loop: sum 0 to 999,999 | 223.75 | 223.28 | 226.02 | 226.65 | 4,469,216 | 18.2 | PASS | Mean 223.75 ms within threshold (500 ms) | -0.5% (stable) |
| BR006 | conditional_branching | Conditional if/else branching: 1,000,000 iterations | 332.39 | 331.06 | 336.98 | 337.47 | 3,008,539 | 18.2 | PASS | Mean 332.39 ms within threshold (500 ms) | +0.4% (stable) |
| BR007 | pattern_matching | Pattern matching (match/case): 100,000 iterations | 31.84 | 31.79 | 32.25 | 32.47 | 3,140,348 | 18.2 | PASS | Mean 31.84 ms within threshold (500 ms) | +0.0% (stable) |
| BR008 | variable_access | Variable access speed: 5 variables, 1,000,000 iterations | 550.87 | 547.90 | 563.86 | 571.91 | 1,815,320 | 18.2 | FAIL | Mean exceeded threshold (500 ms). Measured: 550.87 ms | +0.0% (stable) |
| BR009 | constant_access | Constant access speed: 3 constants, 1,000,000 iterations | 371.89 | 370.80 | 377.17 | 380.02 | 2,688,973 | 18.2 | PASS | Mean 371.89 ms within threshold (500 ms) | -0.0% (stable) |
### Collections

| ID | Benchmark | Description | Mean (ms) | Median | P95 | P99 | Throughput (ops/s) | Mem (MB) | Status | Reason | Regression |
|----|----------|-------------|-----------|--------|-----|-----|---------------------|----------|--------|--------|------------|
| BR010 | array_create | Array creation: 10,000 array literal allocations | 3.41 | 3.39 | 3.47 | 3.48 | 2,936,254 | 18.2 | PASS | Mean 3.41 ms within threshold (100 ms) | +0.8% (stable) |
| BR011 | array_push | Array push: 100,000 push operations | 41.83 | 41.73 | 42.26 | 42.27 | 2,390,492 | 18.2 | PASS | Mean 41.83 ms within threshold (1000 ms) | +1.5% (stable) |
| BR012 | array_access | Array index access: 10,000 elements, 10,000 reads | 8.11 | 8.09 | 8.24 | 8.25 | 1,232,407 | 18.2 | PASS | Mean 8.11 ms within threshold (500 ms) | +1.6% (stable) |
| BR013 | array_iterate | Array for-in iteration: 10,000 elements | 6.12 | 6.11 | 6.20 | 6.22 | 1,633,907 | 18.2 | PASS | Mean 6.12 ms within threshold (500 ms) | +1.4% (stable) |
### Strings

| ID | Benchmark | Description | Mean (ms) | Median | P95 | P99 | Throughput (ops/s) | Mem (MB) | Status | Reason | Regression |
|----|----------|-------------|-----------|--------|-----|-----|---------------------|----------|--------|--------|------------|
| BR014 | string_create | String creation: 10,000 string assignments | 2.72 | 2.72 | 2.76 | 2.77 | 3,678,229 | 18.2 | PASS | Mean 2.72 ms within threshold (100 ms) | +1.9% (stable) |
| BR015 | string_concat | String concatenation: 10,000 appends with + | 8.18 | 8.16 | 8.28 | 8.30 | 1,222,972 | 18.2 | PASS | Mean 8.18 ms within threshold (500 ms) | +1.5% (stable) |
| BR016 | string_len | String length: len() called 1,000,000 times | 374.12 | 367.97 | 402.52 | 422.34 | 2,672,972 | 18.2 | PASS | Mean 374.12 ms within threshold (1000 ms) | +1.3% (stable) |
### Math

| ID | Benchmark | Description | Mean (ms) | Median | P95 | P99 | Throughput (ops/s) | Mem (MB) | Status | Reason | Regression |
|----|----------|-------------|-----------|--------|-----|-----|---------------------|----------|--------|--------|------------|
| BR017 | integer_arithmetic | Integer arithmetic (+, -, *, /): 1,000,000 iterations | 409.19 | 407.72 | 415.74 | 415.99 | 2,443,842 | 18.2 | PASS | Mean 409.19 ms within threshold (1000 ms) | +0.2% (stable) |
| BR018 | float_arithmetic | Float arithmetic: 1,000,000 iterations | 273.14 | 272.57 | 275.60 | 276.47 | 3,661,140 | 18.2 | PASS | Mean 273.14 ms within threshold (1000 ms) | -0.8% (stable) |
| BR019 | power_operation | Power operation (**): 100,000 iterations | 24.66 | 24.20 | 26.69 | 28.24 | 4,054,673 | 18.2 | PASS | Mean 24.66 ms within threshold (500 ms) | +1.7% (stable) |
| BR020 | modulo_operation | Modulo operation (%): 1,000,000 iterations | 265.57 | 265.32 | 267.95 | 268.08 | 3,765,500 | 18.2 | PASS | Mean 265.57 ms within threshold (1000 ms) | -0.1% (stable) |
### Error Handling

| ID | Benchmark | Description | Mean (ms) | Median | P95 | P99 | Throughput (ops/s) | Mem (MB) | Status | Reason | Regression |
|----|----------|-------------|-----------|--------|-----|-----|---------------------|----------|--------|--------|------------|
| BR021 | try_catch_overhead | Try/catch block overhead: 100,000 iterations (no throw) | 0.47 | 0.46 | 0.51 | 0.52 | 213,174,163 | 18.2 | PASS | Mean 0.47 ms within threshold (100 ms) | +2.5% (stable) |
### Compiler

| ID | Benchmark | Description | Mean (ms) | Median | P95 | P99 | Throughput (ops/s) | Mem (MB) | Status | Reason | Regression |
|----|----------|-------------|-----------|--------|-----|-----|---------------------|----------|--------|--------|------------|
| BR022 | parse_large_program | Parser speed: 10 function definitions + call | 0.46 | 0.45 | 0.51 | 0.53 | 2,156 | 18.2 | PASS | Mean 0.46 ms within threshold (10 ms) | +3.2% (stable) |
### Stress Test

| ID | Benchmark | Description | Mean (ms) | Median | P95 | P99 | Throughput (ops/s) | Mem (MB) | Status | Reason | Regression |
|----|----------|-------------|-----------|--------|-----|-----|---------------------|----------|--------|--------|------------|
| BR023 | stress_deep_recursion | Deep recursion: 500 levels | 0.81 | 0.81 | 0.84 | 0.84 | 616,295 | 18.2 | PASS | Mean 0.81 ms within threshold (1000 ms) | +4.9% (stable) |
| BR024 | stress_large_array | Large array: 100,000 push operations | 41.76 | 41.76 | 42.06 | 42.11 | 2,394,854 | 18.2 | PASS | Mean 41.76 ms within threshold (5000 ms) | +1.4% (stable) |
| BR025 | stress_many_calls | Many function calls: 1,000,000 noop calls | 404.16 | 400.49 | 420.65 | 430.15 | 2,474,273 | 18.2 | PASS | Mean 404.16 ms within threshold (2000 ms) | -0.0% (stable) |
| BR026 | stress_large_loop | Large loop: 10,000,000 iterations | 1984.22 | 1969.36 | 2051.69 | 2052.70 | 5,039,772 | 18.2 | PASS | Mean 1984.22 ms within threshold (10000 ms) | +0.8% (stable) |

---

## Final Analysis

### Performance Strengths
- Fastest benchmark: **startup_shutdown** (0.44 ms)
- Overall pass rate: 25/26 (96%)
- Correct output verified for all passing benchmarks
- Low variance (stdev < 5% of mean) for most benchmarks

### Performance Weaknesses
- Slowest benchmark: **stress_large_loop** (1984.22 ms)
- 1 benchmark(s) failed:
  - BR008 variable_access: Mean exceeded threshold (500 ms). Measured: 550.87 ms

### Optimization Suggestions
- [Planned] Bytecode compilation (.sibc format) — estimated 3-5x speedup
- [Planned] JIT compilation for hot-path functions
- [Planned] Optimize array push() with pre-allocation strategy
- [Planned] Use SIMD instructions for batch array operations
- [Planned] Cache string length instead of recalculating

### Known Issues
- Integer overflow on large sums (32-bit int without overflow detection)
- try/catch blocks are parsed but not fully evaluated

### Future Improvements
- [Planned] Native code generation (LLVM backend) — target: near-C performance
- [Planned] Incremental compilation for faster rebuilds
- [Planned] Parallel garbage collection
- [Planned] Async I/O for file and network operations

## Methodology

- Each benchmark runs **10 times** after **2 warmup** runs
- Statistics: mean, median, min, max, stdev, P50, P90, P95, P99
- 95% confidence interval calculated using t-distribution
- Outlier detection: IQR method (1.5x interquartile range)
- Correctness: each benchmark verifies expected output
- Memory: peak RSS measured via getrusage
- CPU: user time and system time measured via getrusage
- Throughput: operations per second = iterations / (mean_ms / 1000)
- Regression: compared with previous run, >5% change flagged
