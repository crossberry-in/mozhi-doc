# Mozhi Performance Benchmark Report

**Benchmark Version:** 3.0.0  
**Date:** 2026-08-01 16:15:18  
**Mozhi Version:** Mozhi v2.0 (C++/ASM/Rust Implementation)  
**Build Hash:** 37b0750b33b9d03b  
**Git Commit:** cfd3754  
**Build Mode:** Release (-O3 -march=native)  
**Interpreter Hash:** 20ba7a1522760a7c  
**Binary Size:** 62.7 KB  

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
| RAM Available | 3492 MB |
| Disk Type | unknown |
| Filesystem | 17% |
| Page Size | 4096 bytes |
| NUMA Nodes | 0 |
| Locale | unknown |
| Timezone | UTC |
| Runs per benchmark | 10 (warmup: 2) |

## Performance Scores

| Category | Score |
|----------|-------|
| Runtime | 65.1 / 100 |
| Collections | 82.3 / 100 |
| Strings | 68.1 / 100 |
| Math | 63.4 / 100 |
| Compiler | 100.0 / 100 |
| Error Handling | 100.0 / 100 |
| **Overall** | **76.6 / 100** |

---

## Detailed Results

### Core Runtime

| ID | Benchmark | Description | Mean (ms) | Median | P95 | P99 | Throughput (ops/s) | Mem (MB) | Status | Reason | Regression |
|----|----------|-------------|-----------|--------|-----|-----|---------------------|----------|--------|--------|------------|
| BR001 | startup_shutdown | Program startup and shutdown time (echo single value) | 0.47 | 0.48 | 0.51 | 0.52 | 2,125 | 18.3 | PASS | Mean 0.47 ms within threshold (100 ms) | +7.8% (regression) |
| BR002 | function_call | Function call overhead: 100,000 calls to add(a,b) | 59.01 | 58.89 | 59.47 | 59.59 | 1,694,611 | 18.3 | PASS | Mean 59.01 ms within threshold (500 ms) | +5.5% (regression) |
| BR003 | recursive_fibonacci | Recursive Fibonacci(25): tests function call + recursion | 100.69 | 100.00 | 104.05 | 106.49 | 2,411,136 | 18.3 | PASS | Mean 100.69 ms within threshold (5000 ms) | +5.1% (regression) |
| BR004 | nested_calls | Nested function calls (5 levels deep): 100,000 iterations | 160.16 | 159.77 | 162.09 | 163.48 | 624,379 | 18.3 | PASS | Mean 160.16 ms within threshold (500 ms) | +6.6% (regression) |
| BR005 | loop_sum | Simple loop: sum 0 to 999,999 | 250.56 | 249.82 | 253.68 | 255.17 | 3,991,001 | 18.3 | PASS | Mean 250.56 ms within threshold (500 ms) | +12.0% (regression) |
| BR006 | conditional_branching | Conditional if/else branching: 1,000,000 iterations | 386.73 | 373.50 | 443.65 | 485.59 | 2,585,805 | 18.3 | PASS | Mean 386.73 ms within threshold (500 ms) | +16.3% (regression) |
| BR007 | pattern_matching | Pattern matching (match/case): 100,000 iterations | 35.93 | 35.89 | 36.15 | 36.17 | 2,783,252 | 18.3 | PASS | Mean 35.93 ms within threshold (500 ms) | +12.8% (regression) |
| BR008 | variable_access | Variable access speed: 5 variables, 1,000,000 iterations | 534.79 | 534.11 | 539.08 | 540.54 | 1,869,909 | 18.3 | FAIL | Mean exceeded threshold (500 ms). Measured: 534.79 ms | -2.9% (stable) |
| BR009 | constant_access | Constant access speed: 3 constants, 1,000,000 iterations | 387.85 | 386.10 | 396.00 | 401.03 | 2,578,333 | 18.3 | PASS | Mean 387.85 ms within threshold (500 ms) | +4.3% (stable) |
### Collections

| ID | Benchmark | Description | Mean (ms) | Median | P95 | P99 | Throughput (ops/s) | Mem (MB) | Status | Reason | Regression |
|----|----------|-------------|-----------|--------|-----|-----|---------------------|----------|--------|--------|------------|
| BR010 | array_create | Array creation: 10,000 array literal allocations | 3.53 | 3.53 | 3.55 | 3.56 | 2,835,351 | 18.3 | PASS | Mean 3.53 ms within threshold (100 ms) | +3.6% (stable) |
| BR011 | array_push | Array push: 100,000 push operations | 42.70 | 42.72 | 42.98 | 43.03 | 2,342,063 | 18.3 | PASS | Mean 42.70 ms within threshold (1000 ms) | +2.1% (stable) |
| BR012 | array_access | Array index access: 10,000 elements, 10,000 reads | 8.31 | 8.28 | 8.47 | 8.51 | 1,203,283 | 18.3 | PASS | Mean 8.31 ms within threshold (500 ms) | +2.4% (stable) |
| BR013 | array_iterate | Array for-in iteration: 10,000 elements | 6.36 | 6.35 | 6.50 | 6.52 | 1,571,462 | 18.3 | PASS | Mean 6.36 ms within threshold (500 ms) | +4.0% (stable) |
### Strings

| ID | Benchmark | Description | Mean (ms) | Median | P95 | P99 | Throughput (ops/s) | Mem (MB) | Status | Reason | Regression |
|----|----------|-------------|-----------|--------|-----|-----|---------------------|----------|--------|--------|------------|
| BR014 | string_create | String creation: 10,000 string assignments | 2.93 | 2.92 | 2.97 | 2.98 | 3,416,818 | 18.3 | PASS | Mean 2.93 ms within threshold (100 ms) | +7.7% (regression) |
| BR015 | string_concat | String concatenation: 10,000 appends with + | 8.37 | 8.37 | 8.43 | 8.45 | 1,194,158 | 18.3 | PASS | Mean 8.37 ms within threshold (500 ms) | +2.4% (stable) |
| BR016 | string_len | String length: len() called 1,000,000 times | 390.88 | 389.89 | 395.49 | 395.84 | 2,558,299 | 18.7 | PASS | Mean 390.88 ms within threshold (1000 ms) | +4.5% (stable) |
### Math

| ID | Benchmark | Description | Mean (ms) | Median | P95 | P99 | Throughput (ops/s) | Mem (MB) | Status | Reason | Regression |
|----|----------|-------------|-----------|--------|-----|-----|---------------------|----------|--------|--------|------------|
| BR017 | integer_arithmetic | Integer arithmetic (+, -, *, /): 1,000,000 iterations | 445.91 | 445.74 | 449.11 | 450.91 | 2,242,628 | 18.7 | PASS | Mean 445.91 ms within threshold (1000 ms) | +9.0% (regression) |
| BR018 | float_arithmetic | Float arithmetic: 1,000,000 iterations | 313.37 | 312.98 | 315.82 | 317.08 | 3,191,099 | 18.7 | PASS | Mean 313.37 ms within threshold (1000 ms) | +14.7% (regression) |
| BR019 | power_operation | Power operation (**): 100,000 iterations | 27.16 | 27.18 | 27.25 | 27.27 | 3,682,061 | 18.7 | PASS | Mean 27.16 ms within threshold (500 ms) | +10.1% (regression) |
| BR020 | modulo_operation | Modulo operation (%): 1,000,000 iterations | 320.00 | 295.71 | 412.90 | 439.94 | 3,124,952 | 18.7 | PASS | Mean 320.00 ms within threshold (1000 ms) | +20.5% (regression) |
### Error Handling

| ID | Benchmark | Description | Mean (ms) | Median | P95 | P99 | Throughput (ops/s) | Mem (MB) | Status | Reason | Regression |
|----|----------|-------------|-----------|--------|-----|-----|---------------------|----------|--------|--------|------------|
| BR021 | try_catch_overhead | Try/catch block overhead: 100,000 iterations (no throw) | 0.48 | 0.48 | 0.51 | 0.53 | 209,555,742 | 18.7 | PASS | Mean 0.48 ms within threshold (100 ms) | +1.7% (stable) |
### Compiler

| ID | Benchmark | Description | Mean (ms) | Median | P95 | P99 | Throughput (ops/s) | Mem (MB) | Status | Reason | Regression |
|----|----------|-------------|-----------|--------|-----|-----|---------------------|----------|--------|--------|------------|
| BR022 | parse_large_program | Parser speed: 10 function definitions + call | 0.48 | 0.48 | 0.51 | 0.52 | 2,076 | 18.7 | PASS | Mean 0.48 ms within threshold (10 ms) | +3.8% (stable) |
### Stress Test

| ID | Benchmark | Description | Mean (ms) | Median | P95 | P99 | Throughput (ops/s) | Mem (MB) | Status | Reason | Regression |
|----|----------|-------------|-----------|--------|-----|-----|---------------------|----------|--------|--------|------------|
| BR023 | stress_deep_recursion | Deep recursion: 500 levels | 0.87 | 0.86 | 0.92 | 0.94 | 575,573 | 18.7 | PASS | Mean 0.87 ms within threshold (1000 ms) | +7.1% (regression) |
| BR024 | stress_large_array | Large array: 100,000 push operations | 43.25 | 43.22 | 43.72 | 43.75 | 2,312,176 | 18.7 | PASS | Mean 43.25 ms within threshold (5000 ms) | +3.6% (stable) |
| BR025 | stress_many_calls | Many function calls: 1,000,000 noop calls | 439.51 | 439.24 | 442.07 | 442.95 | 2,275,249 | 18.7 | PASS | Mean 439.51 ms within threshold (2000 ms) | +8.7% (regression) |
| BR026 | stress_large_loop | Large loop: 10,000,000 iterations | 2239.55 | 2233.25 | 2270.25 | 2285.69 | 4,465,190 | 18.7 | PASS | Mean 2239.55 ms within threshold (10000 ms) | +12.9% (regression) |

---

## Final Analysis

### Performance Strengths
- Fastest benchmark: **startup_shutdown** (0.47 ms)
- Overall pass rate: 25/26 (96%)
- Correct output verified for all passing benchmarks
- Low variance (stdev < 5% of mean) for most benchmarks

### Performance Weaknesses
- Slowest benchmark: **stress_large_loop** (2239.55 ms)
- 1 benchmark(s) failed:
  - BR008 variable_access: Mean exceeded threshold (500 ms). Measured: 534.79 ms

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
