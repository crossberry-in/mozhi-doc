# Sino Performance Benchmark Report

**Benchmark Version:** 2.0.0  
**Date:** 2026-08-01 12:09:59  
**Sino Version:** Sino v1.0 (C Implementation)  
**Build Hash:** 817cc1b5c13547a5  
**Git Commit:** 624c22f  
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
| RAM Available | 3586 MB |
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
| Collections | 82.5 / 100 |
| Strings | 68.5 / 100 |
| Math | 64.2 / 100 |
| Compiler | 100.0 / 100 |
| Error Handling | 100.0 / 100 |
| **Overall** | **77.0 / 100** |

---

## Detailed Results

### Core Runtime

| ID | Benchmark | Description | Mean (ms) | Median | P95 | P99 | Throughput (ops/s) | Mem (MB) | Status | Reason | Regression |
|----|----------|-------------|-----------|--------|-----|-----|---------------------|----------|--------|--------|------------|
| BR001 | startup_shutdown | Program startup and shutdown time (echo single value) | 0.42 | 0.43 | 0.45 | 0.45 | 2,366 | 17.8 | PASS | Mean 0.42 ms within threshold (100 ms) | -14.6% (improved) |
| BR002 | function_call | Function call overhead: 100,000 calls to add(a,b) | 55.04 | 54.95 | 55.46 | 55.58 | 1,816,834 | 17.8 | PASS | Mean 55.04 ms within threshold (500 ms) | -1.0% (stable) |
| BR003 | recursive_fibonacci | Recursive Fibonacci(25): tests function call + recursion | 95.97 | 95.53 | 98.13 | 99.45 | 2,529,740 | 17.8 | PASS | Mean 95.97 ms within threshold (5000 ms) | -6.2% (improved) |
| BR004 | nested_calls | Nested function calls (5 levels deep): 100,000 iterations | 149.25 | 149.22 | 149.79 | 149.82 | 670,023 | 17.8 | PASS | Mean 149.25 ms within threshold (500 ms) | -0.2% (stable) |
| BR005 | loop_sum | Simple loop: sum 0 to 999,999 | 224.83 | 223.99 | 229.36 | 229.77 | 4,447,785 | 17.8 | PASS | Mean 224.83 ms within threshold (500 ms) | +0.8% (stable) |
| BR006 | conditional_branching | Conditional if/else branching: 1,000,000 iterations | 331.22 | 329.54 | 336.71 | 337.01 | 3,019,162 | 17.8 | PASS | Mean 331.22 ms within threshold (500 ms) | +0.6% (stable) |
| BR007 | pattern_matching | Pattern matching (match/case): 100,000 iterations | 31.83 | 31.60 | 32.66 | 32.89 | 3,141,641 | 17.8 | PASS | Mean 31.83 ms within threshold (500 ms) | +0.3% (stable) |
| BR008 | variable_access | Variable access speed: 5 variables, 1,000,000 iterations | 550.63 | 549.58 | 556.90 | 557.34 | 1,816,113 | 17.8 | FAIL | Mean exceeded threshold (500 ms). Measured: 550.63 ms | -0.1% (stable) |
| BR009 | constant_access | Constant access speed: 3 constants, 1,000,000 iterations | 372.01 | 370.39 | 378.68 | 381.47 | 2,688,124 | 17.8 | PASS | Mean 372.01 ms within threshold (500 ms) | -0.6% (stable) |
### Collections

| ID | Benchmark | Description | Mean (ms) | Median | P95 | P99 | Throughput (ops/s) | Mem (MB) | Status | Reason | Regression |
|----|----------|-------------|-----------|--------|-----|-----|---------------------|----------|--------|--------|------------|
| BR010 | array_create | Array creation: 10,000 array literal allocations | 3.38 | 3.38 | 3.41 | 3.41 | 2,959,981 | 17.8 | PASS | Mean 3.38 ms within threshold (100 ms) | -2.8% (stable) |
| BR011 | array_push | Array push: 100,000 push operations | 41.21 | 41.16 | 41.47 | 41.51 | 2,426,731 | 17.8 | PASS | Mean 41.21 ms within threshold (1000 ms) | -1.8% (stable) |
| BR012 | array_access | Array index access: 10,000 elements, 10,000 reads | 7.99 | 7.98 | 8.09 | 8.09 | 1,251,627 | 17.8 | PASS | Mean 7.99 ms within threshold (500 ms) | -0.6% (stable) |
| BR013 | array_iterate | Array for-in iteration: 10,000 elements | 6.04 | 6.04 | 6.09 | 6.10 | 1,656,918 | 17.8 | PASS | Mean 6.04 ms within threshold (500 ms) | -3.0% (stable) |
### Strings

| ID | Benchmark | Description | Mean (ms) | Median | P95 | P99 | Throughput (ops/s) | Mem (MB) | Status | Reason | Regression |
|----|----------|-------------|-----------|--------|-----|-----|---------------------|----------|--------|--------|------------|
| BR014 | string_create | String creation: 10,000 string assignments | 2.67 | 2.67 | 2.68 | 2.68 | 3,746,301 | 17.8 | PASS | Mean 2.67 ms within threshold (100 ms) | -4.6% (stable) |
| BR015 | string_concat | String concatenation: 10,000 appends with + | 8.05 | 8.05 | 8.10 | 8.11 | 1,241,804 | 17.8 | PASS | Mean 8.05 ms within threshold (500 ms) | -1.4% (stable) |
| BR016 | string_len | String length: len() called 1,000,000 times | 369.41 | 368.93 | 373.67 | 374.96 | 2,707,005 | 17.8 | PASS | Mean 369.41 ms within threshold (1000 ms) | +0.1% (stable) |
### Math

| ID | Benchmark | Description | Mean (ms) | Median | P95 | P99 | Throughput (ops/s) | Mem (MB) | Status | Reason | Regression |
|----|----------|-------------|-----------|--------|-----|-----|---------------------|----------|--------|--------|------------|
| BR017 | integer_arithmetic | Integer arithmetic (+, -, *, /): 1,000,000 iterations | 408.41 | 408.09 | 411.08 | 411.98 | 2,448,531 | 17.8 | PASS | Mean 408.41 ms within threshold (1000 ms) | -0.5% (stable) |
| BR018 | float_arithmetic | Float arithmetic: 1,000,000 iterations | 275.37 | 273.50 | 281.79 | 281.98 | 3,631,424 | 17.8 | PASS | Mean 275.37 ms within threshold (1000 ms) | +0.2% (stable) |
| BR019 | power_operation | Power operation (**): 100,000 iterations | 24.25 | 24.18 | 24.48 | 24.49 | 4,124,154 | 17.8 | PASS | Mean 24.25 ms within threshold (500 ms) | +0.0% (stable) |
| BR020 | modulo_operation | Modulo operation (%): 1,000,000 iterations | 265.79 | 265.04 | 268.98 | 269.20 | 3,762,323 | 17.8 | PASS | Mean 265.79 ms within threshold (1000 ms) | -0.1% (stable) |
### Error Handling

| ID | Benchmark | Description | Mean (ms) | Median | P95 | P99 | Throughput (ops/s) | Mem (MB) | Status | Reason | Regression |
|----|----------|-------------|-----------|--------|-----|-----|---------------------|----------|--------|--------|------------|
| BR021 | try_catch_overhead | Try/catch block overhead: 100,000 iterations (no throw) | 0.46 | 0.45 | 0.48 | 0.48 | 218,483,723 | 17.8 | PASS | Mean 0.46 ms within threshold (100 ms) | -6.7% (improved) |
### Compiler

| ID | Benchmark | Description | Mean (ms) | Median | P95 | P99 | Throughput (ops/s) | Mem (MB) | Status | Reason | Regression |
|----|----------|-------------|-----------|--------|-----|-----|---------------------|----------|--------|--------|------------|
| BR022 | parse_large_program | Parser speed: 10 function definitions + call | 0.45 | 0.45 | 0.47 | 0.47 | 2,225 | 17.8 | PASS | Mean 0.45 ms within threshold (10 ms) | -7.0% (improved) |
### Stress Test

| ID | Benchmark | Description | Mean (ms) | Median | P95 | P99 | Throughput (ops/s) | Mem (MB) | Status | Reason | Regression |
|----|----------|-------------|-----------|--------|-----|-----|---------------------|----------|--------|--------|------------|
| BR023 | stress_deep_recursion | Deep recursion: 500 levels | 0.77 | 0.77 | 0.82 | 0.83 | 646,329 | 17.8 | PASS | Mean 0.77 ms within threshold (1000 ms) |  |
| BR024 | stress_large_array | Large array: 100,000 push operations | 41.17 | 41.21 | 41.62 | 41.73 | 2,428,682 | 17.8 | PASS | Mean 41.17 ms within threshold (5000 ms) |  |
| BR025 | stress_many_calls | Many function calls: 1,000,000 noop calls | 404.23 | 399.74 | 421.75 | 421.83 | 2,473,820 | 17.8 | PASS | Mean 404.23 ms within threshold (2000 ms) |  |
| BR026 | stress_large_loop | Large loop: 10,000,000 iterations | 1968.01 | 1964.76 | 1982.53 | 1986.02 | 5,081,264 | 17.8 | PASS | Mean 1968.01 ms within threshold (10000 ms) |  |

---

## Final Analysis

### Performance Strengths
- Fastest benchmark: **startup_shutdown** (0.42 ms)
- Overall pass rate: 25/26 (96%)
- Correct output verified for all passing benchmarks
- Low variance (stdev < 5% of mean) for most benchmarks

### Performance Weaknesses
- Slowest benchmark: **stress_large_loop** (1968.01 ms)
- 1 benchmark(s) failed:
  - BR008 variable_access: Mean exceeded threshold (500 ms). Measured: 550.63 ms

### Optimization Suggestions
- Implement bytecode compilation for 3-5x speedup
- Add JIT compilation for hot-path functions
- Optimize array push() with pre-allocation strategy
- Use SIMD instructions for batch array operations
- Cache string length instead of recalculating

### Known Issues
- Integer overflow on large sums (32-bit int without overflow detection)
- try/catch blocks are parsed but not fully evaluated

### Future Improvements
- Native code generation (LLVM backend) for near-C performance
- Incremental compilation for faster rebuilds
- Parallel garbage collection
- Async I/O for file and network operations

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
