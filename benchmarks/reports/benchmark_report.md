# Sino Performance Benchmark Report

**Version:** 1.0.0  
**Date:** 2026-08-01 10:04:25  
**OS:** Linux 5.10.134-013.8.3.kangaroo.al8.x86_64  
**Architecture:** x86_64  
**CPU:** Intel(R) Xeon(R) Processor  
**Cores:** 2  
**RAM:** 4041 MB  
**Sino Version:** unknown  
**Runs per benchmark:** 10 (warmup: 2)

---

## Results

### Core Runtime

| Benchmark | Mean (ms) | Median | Min | Max | Stdev | Status |
|-----------|-----------|--------|-----|-----|-------|--------|
| startup_shutdown | 0.49 | 0.49 | 0.46 | 0.55 | 0.02 | PASS |
| function_call | 55.57 | 55.31 | 54.75 | 57.29 | 0.79 | FAIL |
| recursive_fibonacci | 102.37 | 96.02 | 95.65 | 127.65 | 11.92 | PASS |
| nested_calls | 149.54 | 149.39 | 148.80 | 150.55 | 0.60 | FAIL |
| loop_sum | 223.15 | 223.11 | 221.90 | 225.22 | 0.87 | PASS |
| conditional_branching | 329.18 | 328.62 | 328.39 | 331.04 | 1.10 | PASS |
| pattern_matching | 31.75 | 31.70 | 31.51 | 32.18 | 0.22 | PASS |
| variable_access | 551.15 | 550.89 | 548.93 | 553.78 | 1.42 | FAIL |
| constant_access | 374.07 | 372.31 | 371.38 | 386.33 | 4.50 | FAIL |
### Collections

| Benchmark | Mean (ms) | Median | Min | Max | Stdev | Status |
|-----------|-----------|--------|-----|-----|-------|--------|
| array_create | 3.48 | 3.45 | 3.40 | 3.65 | 0.07 | FAIL |
| array_push | 41.95 | 41.71 | 41.28 | 43.10 | 0.64 | PASS |
| array_access | 8.04 | 7.99 | 7.93 | 8.40 | 0.14 | PASS |
| array_iterate | 6.22 | 6.20 | 6.14 | 6.39 | 0.07 | PASS |
### Strings

| Benchmark | Mean (ms) | Median | Min | Max | Stdev | Status |
|-----------|-----------|--------|-----|-----|-------|--------|
| string_create | 2.80 | 2.77 | 2.72 | 2.92 | 0.07 | FAIL |
| string_concat | 8.16 | 8.16 | 8.10 | 8.24 | 0.04 | FAIL |
| string_len | 368.93 | 368.12 | 367.07 | 376.80 | 2.92 | PASS |
### Math

| Benchmark | Mean (ms) | Median | Min | Max | Stdev | Status |
|-----------|-----------|--------|-----|-----|-------|--------|
| integer_arithmetic | 410.36 | 409.28 | 408.11 | 419.31 | 3.36 | FAIL |
| float_arithmetic | 274.79 | 272.72 | 272.26 | 282.72 | 3.88 | FAIL |
| power_operation | 24.25 | 24.21 | 24.12 | 24.58 | 0.12 | PASS |
| modulo_operation | 266.16 | 264.86 | 264.40 | 273.92 | 3.09 | FAIL |
### Error Handling

| Benchmark | Mean (ms) | Median | Min | Max | Stdev | Status |
|-----------|-----------|--------|-----|-----|-------|--------|
| try_catch_overhead | 0.49 | 0.50 | 0.45 | 0.53 | 0.03 | FAIL |
### Compiler

| Benchmark | Mean (ms) | Median | Min | Max | Stdev | Status |
|-----------|-----------|--------|-----|-----|-------|--------|
| parse_large_program | 0.48 | 0.48 | 0.46 | 0.51 | 0.02 | PASS |

---

## Summary

- **Total benchmarks:** 22
- **Passed:** 11
- **Failed:** 11

## Methodology

- Each benchmark runs 10 times after 2 warmup runs
- Statistics: mean, median, min, max, standard deviation, 95% confidence interval
- Outlier detection: IQR method (1.5x interquartile range)
- Correctness: each benchmark verifies expected output
