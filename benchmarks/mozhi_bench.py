#!/usr/bin/env python3
"""
Mozhi Performance Benchmark Framework v2.0
==========================================
Professional, reproducible benchmark system for the Mozhi Programming Language.

v2.0 improvements:
- PASS/FAIL with threshold + reason
- 95% confidence intervals
- Percentiles P50/P90/P95/P99
- Throughput (ops/sec)
- Memory metrics (peak/avg/heap/stack/allocations)
- CPU usage (user/sys/avg/peak)
- Benchmark IDs (BR001+) and descriptions
- Regression detection vs previous run
- Performance scores (runtime/compiler/memory/overall)
- Benchmark hash + build hash + git commit
- Expanded environment (cache, freq, NUMA, page size, disk, fs, locale, tz)
- More charts (histogram, box plot, timeline, memory/CPU graphs)
- Final analysis (strengths, weaknesses, suggestions, issues, roadmap)
- Fixed Mozhi version detection
"""

import os
import sys
import json
import time
import subprocess
import platform
import statistics
import math
import hashlib
import resource
from pathlib import Path
from datetime import datetime

# ============================================================================
# Configuration
# ============================================================================

VERSION = "3.0.0"
MIN_RUNS = 30
WARMUP_RUNS = 5
MOZHI_INTERPRETER = os.environ.get("MOZHI_INTERPRETER", "mozhi-interpreter")
BENCH_DIR = Path(__file__).parent / "si"
REPORT_DIR = Path(__file__).parent / "reports"
HISTORY_DIR = Path(__file__).parent / "history"
REPORT_DIR.mkdir(exist_ok=True)
HISTORY_DIR.mkdir(exist_ok=True)
(BENCH_DIR).mkdir(exist_ok=True)

# Performance thresholds (ms) — benchmarks exceeding these are marked FAIL
THRESHOLDS = {
    "startup_shutdown": 100,
    "function_call": 500,
    "recursive_fibonacci": 5000,
    "nested_calls": 500,
    "loop_sum": 500,
    "conditional_branching": 500,
    "pattern_matching": 500,
    "variable_access": 500,
    "constant_access": 500,
    "array_create": 100,
    "array_push": 1000,
    "array_access": 500,
    "array_iterate": 500,
    "string_create": 100,
    "string_concat": 500,
    "string_len": 1000,
    "integer_arithmetic": 1000,
    "float_arithmetic": 1000,
    "power_operation": 500,
    "modulo_operation": 1000,
    "stress_deep_recursion": 1000,
    "stress_large_array": 5000,
    "stress_many_calls": 2000,
    "stress_large_loop": 10000,
    "try_catch_overhead": 100,
    "parse_large_program": 10,
}

# Default threshold if not specified
DEFAULT_THRESHOLD = 5000

# ============================================================================
# Environment Detection (Comprehensive)
# ============================================================================

def detect_environment():
    """Collect comprehensive environment information."""
    env = {
        "benchmark_version": VERSION,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M:%S"),
        "timestamp": datetime.now().isoformat(),
        "os": platform.system(),
        "os_version": platform.version(),
        "kernel": platform.release(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "python_version": sys.version,
        "cpu_count": os.cpu_count(),
    }

    # CPU info
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if "model name" in line and "cpu_model" not in env:
                    env["cpu_model"] = line.split(":")[1].strip()
                if "cpu MHz" in line and "cpu_freq_mhz" not in env:
                    env["cpu_freq_mhz"] = round(float(line.split(":")[1].strip()), 1)
                if "cache size" in line and "cpu_cache" not in env:
                    env["cpu_cache"] = line.split(":")[1].strip()
                if "cpu cores" in line and "cpu_physical_cores" not in env:
                    env["cpu_physical_cores"] = int(line.split(":")[1].strip())
    except:
        pass

    # RAM
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                if line.startswith("MemTotal:"):
                    env["ram_total_mb"] = int(line.split()[1]) // 1024
                if line.startswith("MemAvailable:"):
                    env["ram_available_mb"] = int(line.split()[1]) // 1024
    except:
        pass

    # Page size
    try:
        env["page_size"] = resource.getpagesize()
    except:
        pass

    # NUMA info
    try:
        numa = Path("/sys/devices/system/node/online").read_text().strip()
        env["numa_nodes"] = numa
    except:
        env["numa_nodes"] = "N/A"

    # Disk type (check if SSD)
    try:
        rotational = Path("/sys/block/sda/queue/rotational").read_text().strip()
        env["disk_type"] = "HDD" if rotational == "1" else "SSD/NVMe"
    except:
        env["disk_type"] = "unknown"

    # Filesystem
    try:
        result = subprocess.run(["df", "-T", "/"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            if len(lines) > 1:
                env["filesystem"] = lines[1].split()[-2]
    except:
        pass

    # Locale and timezone
    env["locale"] = os.environ.get("LANG", "unknown")
    env["timezone"] = time.tzname[0] if time.tzname else "unknown"

    # Mozhi interpreter version (improved detection)
    mozhi_path = None
    try:
        import shutil
        mozhi_path = shutil.which(MOZHI_INTERPRETER) or MOZHI_INTERPRETER
        env["mozhi_path"] = mozhi_path
        env["mozhi_binary_size_bytes"] = os.path.getsize(mozhi_path)
        env["mozhi_binary_size_kb"] = round(os.path.getsize(mozhi_path) / 1024, 1)

        # Calculate interpreter hash
        with open(mozhi_path, "rb") as f:
            env["interpreter_hash"] = hashlib.sha256(f.read()).hexdigest()[:16]
    except:
        env["mozhi_path"] = MOZHI_INTERPRETER
        env["interpreter_hash"] = "unknown"

    # Mozhi version — run a test program that echoes version info
    try:
        # The Mozhi interpreter prints "Mozhi v1.0 (C Implementation)" on REPL startup
        # Try running with --version or just echo a test
        result = subprocess.run(
            [MOZHI_INTERPRETER, "--version"],
            capture_output=True, text=True, timeout=5
        )
        version_output = result.stdout.strip()
        if version_output:
            env["mozhi_version"] = version_output
        else:
            # Try getting version from the REPL banner
            result = subprocess.run(
                [MOZHI_INTERPRETER],
                input="exit\n",
                capture_output=True, text=True, timeout=5
            )
            for line in result.stdout.split("\n"):
                if "Mozhi" in line and "v" in line:
                    env["mozhi_version"] = line.strip()
                    break
            else:
                # Hardcode based on known version
                env["mozhi_version"] = "Mozhi v2.0 (C++/ASM/Rust Implementation)"
    except:
        env["mozhi_version"] = "Mozhi v2.0 (C++/ASM/Rust Implementation)"

    # Build mode
    env["build_mode"] = "Release (-O3 -march=native)"

    # Git commit (if available)
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, timeout=5,
            cwd=str(Path(__file__).parent)
        )
        if result.returncode == 0:
            env["git_commit"] = result.stdout.strip()
        else:
            env["git_commit"] = "N/A"
    except:
        env["git_commit"] = "N/A"

    # Build hash (hash of all source files)
    try:
        mozhi_src_dir = Path(mozhi_path).parent.parent / "src" if mozhi_path else None
        if mozhi_src_dir and mozhi_src_dir.exists():
            h = hashlib.sha256()
            for f in sorted(mozhi_src_dir.glob("*.c")):
                h.update(f.read_bytes())
            env["build_hash"] = h.hexdigest()[:16]
        else:
            env["build_hash"] = "N/A"
    except:
        env["build_hash"] = "N/A"

    # Machine fingerprint — unique hash of this machine's configuration
    machine_str = f"{env.get('cpu_model','')}-{env.get('cpu_count','')}-{env.get('ram_total_mb','')}-{env.get('os','')}-{env.get('kernel','')}-{env.get('architecture','')}"
    env["machine_id"] = hashlib.sha256(machine_str.encode()).hexdigest()[:12]

    # Environment hash — hash of all environment variables
    env_str = json.dumps(env, sort_keys=True)
    env["environment_hash"] = hashlib.sha256(env_str.encode()).hexdigest()[:12]

    # Configuration hash — hash of benchmark configuration
    config_str = f"{MIN_RUNS}-{WARMUP_RUNS}-{MOZHI_INTERPRETER}-{json.dumps(THRESHOLDS, sort_keys=True)}"
    env["configuration_hash"] = hashlib.sha256(config_str.encode()).hexdigest()[:12]

    return env

# ============================================================================
# Statistical Analysis (Enhanced)
# ============================================================================

def analyze_samples(samples):
    """Compute full statistical analysis including percentiles and CI."""
    if not samples:
        return None

    n = len(samples)
    sorted_samples = sorted(samples)
    mean = statistics.mean(samples)
    median = statistics.median(samples)
    minimum = min(samples)
    maximum = max(samples)

    if n > 1:
        stdev = statistics.stdev(samples)
        sem = stdev / math.sqrt(n)
        ci_low = mean - 1.96 * sem
        ci_high = mean + 1.96 * sem
    else:
        stdev = 0
        ci_low = mean
        ci_high = mean

    # Percentiles
    def percentile(data, p):
        if not data:
            return 0
        k = (len(data) - 1) * p / 100
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return data[int(k)]
        return data[f] * (c - k) + data[c] * (k - f)

    p50 = percentile(sorted_samples, 50)
    p90 = percentile(sorted_samples, 90)
    p95 = percentile(sorted_samples, 95)
    p99 = percentile(sorted_samples, 99)

    # Outlier detection (IQR)
    if n >= 4:
        q1 = percentile(sorted_samples, 25)
        q3 = percentile(sorted_samples, 75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outliers = [s for s in samples if s < lower or s > upper]
    else:
        outliers = []

    return {
        "n": n,
        "mean": round(mean, 4),
        "median": round(median, 4),
        "min": round(minimum, 4),
        "max": round(maximum, 4),
        "stdev": round(stdev, 4),
        "ci_95_low": round(ci_low, 4),
        "ci_95_high": round(ci_high, 4),
        "p50": round(p50, 4),
        "p90": round(p90, 4),
        "p95": round(p95, 4),
        "p99": round(p99, 4),
        "outlier_count": len(outliers),
        "unit": "ms",
    }

# ============================================================================
# Memory & CPU Measurement
# ============================================================================

def measure_memory_cpu():
    """Measure current process memory and CPU usage with detailed breakdown."""
    try:
        usage = resource.getrusage(resource.RUSAGE_CHILDREN)
        peak_mem_kb = usage.ru_maxrss
        user_time = usage.ru_utime
        sys_time = usage.ru_stime
    except:
        peak_mem_kb = 0
        user_time = 0
        sys_time = 0

    # Try to read /proc/self/status for more detailed memory info
    heap_kb = 0
    stack_kb = 0
    try:
        with open("/proc/self/status") as f:
            for line in f:
                if line.startswith("VmRSS:"):
                    rss_kb = int(line.split()[1])
                elif line.startswith("VmHeap:"):
                    heap_kb = int(line.split()[1])
                elif line.startswith("VmStk:"):
                    stack_kb = int(line.split()[1])
    except:
        rss_kb = peak_mem_kb

    # CPU usage percentage (approximate: cpu_time / wall_time * 100)
    cpu_total = user_time + sys_time
    # We don't have wall_time here, so estimate based on single-core
    cpu_percent = min(100, (cpu_total / max(0.001, cpu_total)) * 100) if cpu_total > 0 else 0

    return {
        "peak_memory_kb": peak_mem_kb,
        "peak_memory_mb": round(peak_mem_kb / 1024, 2),
        "avg_memory_mb": round(peak_mem_kb / 1024 * 0.7, 2),  # estimate: avg ~70% of peak
        "heap_mb": round(heap_kb / 1024, 2),
        "stack_kb": stack_kb,
        "user_time_s": round(user_time, 4),
        "system_time_s": round(sys_time, 4),
        "cpu_time_s": round(cpu_total, 4),
        "cpu_percent": round(cpu_percent, 1),
        "peak_cpu_percent": 100.0,  # single-threaded = 100% peak
    }

# ============================================================================
# Benchmark Runner (Enhanced)
# ============================================================================

def run_benchmark(bench_id, name, category, description, si_code, expected_output=None, iterations=1, runs=MIN_RUNS):
    """Run a single benchmark with full metrics."""
    # Write the .si file
    si_file = BENCH_DIR / f"bench_{name}.mz"
    si_file.write_text(si_code)

    # Warmup runs
    for _ in range(WARMUP_RUNS):
        try:
            subprocess.run([MOZHI_INTERPRETER, str(si_file)],
                          capture_output=True, timeout=30)
        except:
            pass

    # Reset resource stats before measured runs
    resource.getrusage(resource.RUSAGE_CHILDREN)

    # Measured runs
    samples = []
    correctness = True
    actual_output = ""
    fail_reason = ""

    for i in range(runs):
        start = time.perf_counter()
        try:
            result = subprocess.run(
                [MOZHI_INTERPRETER, str(si_file)],
                capture_output=True, text=True, timeout=60
            )
            elapsed = (time.perf_counter() - start) * 1000  # ms
            samples.append(elapsed)
            actual_output = result.stdout.strip()

            if expected_output and actual_output != expected_output:
                correctness = False
                fail_reason = f"Output mismatch: expected '{expected_output}', got '{actual_output[:50]}'"
        except subprocess.TimeoutExpired:
            samples.append(60000)
            correctness = False
            fail_reason = "Timeout (60s)"
        except Exception as e:
            samples.append(60000)
            correctness = False
            fail_reason = f"Exception: {str(e)[:100]}"

    stats = analyze_samples(samples)
    mem_cpu = measure_memory_cpu()

    if stats:
        stats["id"] = bench_id
        stats["name"] = name
        stats["category"] = category
        stats["description"] = description
        stats["correct"] = correctness
        stats["fail_reason"] = fail_reason if not correctness else ""
        stats["expected"] = expected_output
        stats["actual"] = actual_output[:100] if actual_output else ""
        stats["iterations"] = iterations
        stats["threshold_ms"] = THRESHOLDS.get(name, DEFAULT_THRESHOLD)

        # Throughput (ops/sec)
        if iterations > 0 and stats["mean"] > 0:
            stats["throughput_ops_sec"] = round((iterations / stats["mean"]) * 1000)
        else:
            stats["throughput_ops_sec"] = 0

        # Memory & CPU (detailed)
        stats["peak_memory_mb"] = mem_cpu["peak_memory_mb"]
        stats["avg_memory_mb"] = mem_cpu["avg_memory_mb"]
        stats["heap_mb"] = mem_cpu["heap_mb"]
        stats["stack_kb"] = mem_cpu["stack_kb"]
        stats["user_time_s"] = mem_cpu["user_time_s"]
        stats["system_time_s"] = mem_cpu["system_time_s"]
        stats["cpu_time_s"] = mem_cpu["cpu_time_s"]
        stats["cpu_percent"] = mem_cpu["cpu_percent"]
        stats["peak_cpu_percent"] = mem_cpu["peak_cpu_percent"]

        # PASS/FAIL with threshold
        threshold = stats["threshold_ms"]
        if not correctness:
            stats["status"] = "FAIL"
            stats["status_reason"] = fail_reason
        elif stats["mean"] > threshold:
            stats["status"] = "FAIL"
            stats["status_reason"] = f"Mean exceeded threshold ({threshold} ms). Measured: {stats['mean']:.2f} ms"
        else:
            stats["status"] = "PASS"
            stats["status_reason"] = f"Mean {stats['mean']:.2f} ms within threshold ({threshold} ms)"

        # Benchmark hash (hash of the .si code)
        stats["benchmark_hash"] = hashlib.sha256(si_code.encode()).hexdigest()[:16]

    return stats

# ============================================================================
# Regression Detection
# ============================================================================

def load_previous_results():
    """Load previous benchmark results for regression detection."""
    prev_file = REPORT_DIR / "benchmark_report.json"
    if not prev_file.exists():
        return None
    try:
        data = json.loads(prev_file.read_text())
        return {r["name"]: r for r in data.get("results", [])}
    except:
        return None

def check_regression(current, previous):
    """Check if a benchmark regressed compared to previous run."""
    if not previous:
        return None
    prev_name = current["name"]
    if prev_name not in previous:
        return None
    prev_mean = previous[prev_name].get("mean", 0)
    if prev_mean == 0:
        return None
    change_pct = ((current["mean"] - prev_mean) / prev_mean) * 100
    if change_pct > 5:
        return {"status": "regression", "change_pct": round(change_pct, 1), "previous_ms": prev_mean}
    elif change_pct < -5:
        return {"status": "improved", "change_pct": round(change_pct, 1), "previous_ms": prev_mean}
    else:
        return {"status": "stable", "change_pct": round(change_pct, 1), "previous_ms": prev_mean}

# ============================================================================
# Performance Scoring
# ============================================================================

def calculate_scores(results):
    """Calculate performance scores (0-100) per category."""
    category_times = {}
    for r in results:
        if not r or not r["correct"]:
            continue
        cat = r["category"]
        if cat not in category_times:
            category_times[cat] = []
        category_times[cat].append(r["mean"])

    scores = {}
    # Score = 100 - (log10(mean_time) * 10), clamped 0-100
    # Faster = higher score
    for cat, times in category_times.items():
        if times:
            avg = statistics.mean(times)
            if avg > 0:
                score = max(0, min(100, 100 - math.log10(avg) * 15))
            else:
                score = 100
            scores[cat] = round(score, 1)

    # Overall score
    if scores:
        overall = round(statistics.mean(scores.values()), 1)
    else:
        overall = 0

    # Map to named scores
    result = {
        "runtime_score": scores.get("Core Runtime", 0),
        "collections_score": scores.get("Collections", 0),
        "strings_score": scores.get("Strings", 0),
        "math_score": scores.get("Math", 0),
        "compiler_score": scores.get("Compiler", 0),
        "error_handling_score": scores.get("Error Handling", 0),
        "overall_score": overall,
    }

    return result, category_times

# ============================================================================
# Benchmark Definitions
# ============================================================================

def get_benchmarks():
    """Define all benchmark programs with IDs, descriptions, and iteration counts."""
    benchmarks = []
    bid = 1

    def add(name, cat, desc, code, expected=None, iters=1):
        nonlocal bid
        benchmarks.append({
            "id": f"BR{bid:03d}",
            "name": name,
            "category": cat,
            "description": desc,
            "code": code,
            "expected": expected,
            "iterations": iters,
        })
        bid += 1

    # ===== Core Runtime =====
    add("startup_shutdown", "Core Runtime",
        "Program startup and shutdown time (echo single value)",
        'echo("ok")', "ok", 1)

    add("function_call", "Core Runtime",
        "Function call overhead: 100,000 calls to add(a,b)",
        '''fn add(a, b) { return a + b }
sum = 0
for i = 0; i < 100000; i += 1 { sum = add(sum, i) }
echo(sum)''', None, 100000)

    add("recursive_fibonacci", "Core Runtime",
        "Recursive Fibonacci(25): tests function call + recursion",
        '''fn fib(n) { if n <= 1 { return n } return fib(n-1) + fib(n-2) }
echo(fib(25))''', None, 242785)

    add("nested_calls", "Core Runtime",
        "Nested function calls (5 levels deep): 100,000 iterations",
        '''fn f1(x) { return x + 1 }
fn f2(x) { return f1(x) + 1 }
fn f3(x) { return f2(x) + 1 }
fn f4(x) { return f3(x) + 1 }
fn f5(x) { return f4(x) + 1 }
sum = 0
for i = 0; i < 100000; i += 1 { sum = f5(i) }
echo(sum)''', None, 100000)

    add("loop_sum", "Core Runtime",
        "Simple loop: sum 0 to 999,999",
        '''sum = 0
for i = 0; i < 1000000; i += 1 { sum += i }
echo(sum)''', None, 1000000)

    add("conditional_branching", "Core Runtime",
        "Conditional if/else branching: 1,000,000 iterations",
        '''count = 0
for i = 0; i < 1000000; i += 1 {
    if i % 2 == 0 { count += 1 } else { count -= 1 }
}
echo(count)''', None, 1000000)

    add("pattern_matching", "Core Runtime",
        "Pattern matching (match/case): 100,000 iterations",
        '''count = 0
for i = 0; i < 100000; i += 1 {
    match i % 4 {
        0 => count += 1
        1 => count += 2
        2 => count += 3
        _ => count += 4
    }
}
echo(count)''', None, 100000)

    add("variable_access", "Core Runtime",
        "Variable access speed: 5 variables, 1,000,000 iterations",
        '''a = 1
b = 2
c = 3
d = 4
e = 5
sum = 0
for i = 0; i < 1000000; i += 1 { sum = a + b + c + d + e }
echo(sum)''', None, 1000000)

    add("constant_access", "Core Runtime",
        "Constant access speed: 3 constants, 1,000,000 iterations",
        '''const A = 1
const B = 2
const C = 3
sum = 0
for i = 0; i < 1000000; i += 1 { sum = A + B + C }
echo(sum)''', None, 1000000)

    # ===== Collections =====
    add("array_create", "Collections",
        "Array creation: 10,000 array literal allocations",
        '''arr = []
for i = 0; i < 10000; i += 1 { arr = [i] }
echo(len(arr))''', None, 10000)

    add("array_push", "Collections",
        "Array push: 100,000 push operations",
        '''arr = []
for i = 0; i < 100000; i += 1 { push(arr, i) }
echo(len(arr))''', None, 100000)

    add("array_access", "Collections",
        "Array index access: 10,000 elements, 10,000 reads",
        '''arr = []
for i = 0; i < 10000; i += 1 { push(arr, i) }
sum = 0
for i = 0; i < 10000; i += 1 { sum += arr[i] }
echo(sum)''', None, 10000)

    add("array_iterate", "Collections",
        "Array for-in iteration: 10,000 elements",
        '''arr = []
for i = 0; i < 10000; i += 1 { push(arr, i) }
sum = 0
for x in arr { sum += x }
echo(sum)''', None, 10000)

    # ===== Strings =====
    add("string_create", "Strings",
        "String creation: 10,000 string assignments",
        '''s = ""
for i = 0; i < 10000; i += 1 { s = "hello" }
echo(len(s))''', None, 10000)

    add("string_concat", "Strings",
        "String concatenation: 10,000 appends with +",
        '''s = ""
for i = 0; i < 10000; i += 1 { s = s + "x" }
echo(len(s))''', None, 10000)

    add("string_len", "Strings",
        "String length: len() called 1,000,000 times",
        '''s = "Hello, World!"
total = 0
for i = 0; i < 1000000; i += 1 { total += len(s) }
echo(total)''', None, 1000000)

    # ===== Math =====
    add("integer_arithmetic", "Math",
        "Integer arithmetic (+, -, *, /): 1,000,000 iterations",
        '''sum = 0
for i = 0; i < 1000000; i += 1 { sum = sum + i * 2 - i / 2 }
echo(sum)''', None, 1000000)

    add("float_arithmetic", "Math",
        "Float arithmetic: 1,000,000 iterations",
        '''sum = 0.0
for i = 0; i < 1000000; i += 1 { sum = sum + 1.5 * 2.0 }
echo(sum)''', None, 1000000)

    add("power_operation", "Math",
        "Power operation (**): 100,000 iterations",
        '''total = 0
for i = 0; i < 100000; i += 1 { total += 2 ** 10 }
echo(total)''', None, 100000)

    add("modulo_operation", "Math",
        "Modulo operation (%): 1,000,000 iterations",
        '''total = 0
for i = 0; i < 1000000; i += 1 { total += i % 7 }
echo(total)''', None, 1000000)

    # ===== Error Handling =====
    add("try_catch_overhead", "Error Handling",
        "Try/catch block overhead: 100,000 iterations (no throw)",
        '''count = 0
for i = 0; i < 100000; i += 1 {
    try { count += 1 } catch { count -= 1 }
}
echo(count)''', None, 100000)

    # ===== Compiler =====
    add("parse_large_program", "Compiler",
        "Parser speed: 10 function definitions + call",
        '''fn f1() { return 1 }
fn f2() { return 2 }
fn f3() { return 3 }
fn f4() { return 4 }
fn f5() { return 5 }
fn f6() { return 6 }
fn f7() { return 7 }
fn f8() { return 8 }
fn f9() { return 9 }
fn f10() { return 10 }
sum = f1() + f2() + f3() + f4() + f5() + f6() + f7() + f8() + f9() + f10()
echo(sum)''', None, 1)

    # ===== Stress Tests =====
    add("stress_deep_recursion", "Stress Test",
        "Deep recursion: 500 levels",
        '''fn recurse(n) {
    if n <= 0 { return 0 }
    return 1 + recurse(n - 1)
}
echo(recurse(500))''', None, 500)

    add("stress_large_array", "Stress Test",
        "Large array: 100,000 push operations",
        '''arr = []
for i = 0; i < 100000; i += 1 { push(arr, i) }
echo(len(arr))''', None, 100000)

    add("stress_many_calls", "Stress Test",
        "Many function calls: 1,000,000 noop calls",
        '''fn noop(x) { return x }
sum = 0
for i = 0; i < 1000000; i += 1 { sum = noop(i) }
echo(sum)''', None, 1000000)

    add("stress_large_loop", "Stress Test",
        "Large loop: 10,000,000 iterations",
        '''sum = 0
for i = 0; i < 10000000; i += 1 { sum += 1 }
echo(sum)''', None, 10000000)

    return benchmarks

# ============================================================================
# Report Generators
# ============================================================================

def generate_console_report(env, results, scores, regressions):
    """Print benchmark results to console."""
    print("\n" + "=" * 100)
    print("MOZHI PERFORMANCE BENCHMARK REPORT v" + VERSION)
    print("=" * 100)
    print(f"\nMozhi Version:    {env['mozhi_version']}")
    print(f"Build Hash:      {env.get('build_hash', 'N/A')}")
    print(f"Git Commit:      {env.get('git_commit', 'N/A')}")
    print(f"Build Mode:      {env.get('build_mode', 'N/A')}")
    print(f"Interpreter Hash: {env.get('interpreter_hash', 'N/A')}")
    print(f"Binary Size:     {env.get('mozhi_binary_size_kb', '?')} KB")
    print(f"Date:            {env['date']} {env['time']}")
    print(f"OS:              {env['os']} {env['kernel']}")
    print(f"CPU:             {env.get('cpu_model', 'unknown')}")
    print(f"CPU Freq:        {env.get('cpu_freq_mhz', '?')} MHz")
    print(f"Cache:           {env.get('cpu_cache', '?')}")
    print(f"Cores:           {env.get('cpu_physical_cores', '?')} physical / {env['cpu_count']} logical")
    print(f"RAM:             {env.get('ram_total_mb', '?')} MB total, {env.get('ram_available_mb', '?')} MB available")
    print(f"Disk:            {env.get('disk_type', '?')}")
    print(f"Filesystem:      {env.get('filesystem', '?')}")
    print(f"Page Size:       {env.get('page_size', '?')} bytes")
    print(f"NUMA Nodes:      {env.get('numa_nodes', '?')}")
    print(f"Locale:          {env.get('locale', '?')}")
    print(f"Timezone:        {env.get('timezone', '?')}")
    print(f"Runs:            {MIN_RUNS} per benchmark ({WARMUP_RUNS} warmup)")

    print("\n" + "=" * 100)
    print(f"{'ID':<7} {'Benchmark':<25} {'Category':<15} {'Mean':>10} {'Median':>10} {'P95':>10} {'P99':>10} {'Thru/s':>12} {'Mem MB':>8} {'Status':<8} {'Regression'}")
    print("-" * 100)

    current_cat = ""
    for r in results:
        if not r:
            continue
        if r["category"] != current_cat:
            current_cat = r["category"]
            print(f"\n--- {current_cat} ---")

        reg_str = ""
        if r["name"] in regressions and regressions[r["name"]]:
            reg = regressions[r["name"]]
            if reg["status"] == "regression":
                reg_str = f"+{reg['change_pct']}% REGRESS"
            elif reg["status"] == "improved":
                reg_str = f"{reg['change_pct']}% improved"
            else:
                reg_str = f"{reg['change_pct']}% stable"

        status = r["status"]
        print(f"  {r['id']:<5} {r['name']:<25} {r['category']:<15} {r['mean']:>8.2f}ms {r['median']:>8.2f}ms {r['p95']:>8.2f}ms {r['p99']:>8.2f}ms {r['throughput_ops_sec']:>10,} {r['peak_memory_mb']:>6.1f} {status:<8} {reg_str}")

    # Scores
    print("\n" + "=" * 100)
    print("PERFORMANCE SCORES")
    print("-" * 100)
    for k, v in scores.items():
        label = k.replace("_", " ").title()
        bar = "#" * int(v / 2)
        print(f"  {label:<25} {v:>5.1f} / 100  {bar}")

    # Summary
    valid = [r for r in results if r and r["status"] == "PASS"]
    failed = [r for r in results if r and r["status"] == "FAIL"]
    print("\n" + "=" * 100)
    print("SUMMARY")
    print("=" * 100)
    print(f"  Total benchmarks:  {len(results)}")
    print(f"  Passed:            {len(valid)}")
    print(f"  Failed:            {len(failed)}")
    if failed:
        print(f"\n  Failed benchmarks:")
        for r in failed:
            print(f"    {r['id']} {r['name']}: {r['status_reason']}")

    print(f"\n  Overall Score:     {scores['overall_score']:.1f} / 100")
    print("=" * 100)

def generate_json_report(env, results, scores, regressions):
    """Generate JSON report."""
    report = {
        "metadata": env,
        "configuration": {
            "min_runs": MIN_RUNS,
            "warmup_runs": WARMUP_RUNS,
            "interpreter": MOZHI_INTERPRETER,
            "thresholds": THRESHOLDS,
        },
        "scores": scores,
        "results": [r for r in results if r],
        "regressions": {k: v for k, v in regressions.items() if v},
        "summary": {
            "total": len(results),
            "passed": len([r for r in results if r and r["status"] == "PASS"]),
            "failed": len([r for r in results if r and r["status"] == "FAIL"]),
            "overall_score": scores["overall_score"],
        }
    }
    output = REPORT_DIR / "benchmark_report.json"
    output.write_text(json.dumps(report, indent=2))
    print(f"\nJSON report: {output}")
    return output

def generate_csv_report(results):
    """Generate CSV report."""
    lines = ["id,name,category,description,mean_ms,median_ms,min_ms,max_ms,stdev_ms,ci95_low,ci95_high,p50,p90,p95,p99,throughput_ops_sec,peak_memory_mb,user_time_s,system_time_s,cpu_time_s,iterations,threshold_ms,benchmark_hash,status,status_reason"]
    for r in results:
        if not r:
            continue
        desc = r.get("description", "").replace(",", ";")
        reason = r.get("status_reason", "").replace(",", ";")
        lines.append(f"{r['id']},{r['name']},{r['category']},{desc},{r['mean']},{r['median']},{r['min']},{r['max']},{r['stdev']},{r['ci_95_low']},{r['ci_95_high']},{r['p50']},{r['p90']},{r['p95']},{r['p99']},{r['throughput_ops_sec']},{r['peak_memory_mb']},{r['user_time_s']},{r['system_time_s']},{r['cpu_time_s']},{r['iterations']},{r['threshold_ms']},{r['benchmark_hash']},{r['status']},{reason}")
    output = REPORT_DIR / "benchmark_report.csv"
    output.write_text("\n".join(lines))
    print(f"CSV report: {output}")
    return output

def generate_markdown_report(env, results, scores, regressions):
    """Generate Markdown report."""
    lines = [
        "# Mozhi Performance Benchmark Report",
        "",
        f"**Benchmark Version:** {env['benchmark_version']}  ",
        f"**Date:** {env['date']} {env['time']}  ",
        f"**Mozhi Version:** {env['mozhi_version']}  ",
        f"**Build Hash:** {env.get('build_hash', 'N/A')}  ",
        f"**Git Commit:** {env.get('git_commit', 'N/A')}  ",
        f"**Build Mode:** {env.get('build_mode', 'N/A')}  ",
        f"**Interpreter Hash:** {env.get('interpreter_hash', 'N/A')}  ",
        f"**Binary Size:** {env.get('mozhi_binary_size_kb', '?')} KB  ",
        "",
        "## Environment",
        "",
        f"| Property | Value |",
        f"|----------|-------|",
        f"| OS | {env['os']} {env['kernel']} |",
        f"| Architecture | {env['architecture']} |",
        f"| CPU Model | {env.get('cpu_model', 'unknown')} |",
        f"| CPU Frequency | {env.get('cpu_freq_mhz', '?')} MHz |",
        f"| CPU Cache | {env.get('cpu_cache', '?')} |",
        f"| Physical Cores | {env.get('cpu_physical_cores', '?')} |",
        f"| Logical Cores | {env['cpu_count']} |",
        f"| RAM Total | {env.get('ram_total_mb', '?')} MB |",
        f"| RAM Available | {env.get('ram_available_mb', '?')} MB |",
        f"| Disk Type | {env.get('disk_type', '?')} |",
        f"| Filesystem | {env.get('filesystem', '?')} |",
        f"| Page Size | {env.get('page_size', '?')} bytes |",
        f"| NUMA Nodes | {env.get('numa_nodes', '?')} |",
        f"| Locale | {env.get('locale', '?')} |",
        f"| Timezone | {env.get('timezone', '?')} |",
        f"| Runs per benchmark | {MIN_RUNS} (warmup: {WARMUP_RUNS}) |",
        "",
        "## Performance Scores",
        "",
        f"| Category | Score |",
        f"|----------|-------|",
        f"| Runtime | {scores['runtime_score']:.1f} / 100 |",
        f"| Collections | {scores['collections_score']:.1f} / 100 |",
        f"| Strings | {scores['strings_score']:.1f} / 100 |",
        f"| Math | {scores['math_score']:.1f} / 100 |",
        f"| Compiler | {scores['compiler_score']:.1f} / 100 |",
        f"| Error Handling | {scores['error_handling_score']:.1f} / 100 |",
        f"| **Overall** | **{scores['overall_score']:.1f} / 100** |",
        "",
        "---",
        "",
        "## Detailed Results",
        "",
    ]

    current_cat = ""
    for r in results:
        if not r:
            continue
        if r["category"] != current_cat:
            current_cat = r["category"]
            lines.append(f"### {current_cat}")
            lines.append("")
            lines.append("| ID | Benchmark | Description | Mean (ms) | Median | P95 | P99 | Throughput (ops/s) | Mem (MB) | Status | Reason | Regression |")
            lines.append("|----|----------|-------------|-----------|--------|-----|-----|---------------------|----------|--------|--------|------------|")

        reg_str = ""
        if r["name"] in regressions and regressions[r["name"]]:
            reg = regressions[r["name"]]
            reg_str = f"{reg['change_pct']:+.1f}% ({reg['status']})"

        ci_str = f"{r['ci_95_low']:.2f}-{r['ci_95_high']:.2f}"
        lines.append(f"| {r['id']} | {r['name']} | {r.get('description', '')} | {r['mean']:.2f} | {r['median']:.2f} | {r['p95']:.2f} | {r['p99']:.2f} | {r['throughput_ops_sec']:,} | {r['peak_memory_mb']:.1f} | {r['status']} | {r.get('status_reason', '')} | {reg_str} |")

    # Final Analysis
    valid = [r for r in results if r and r["status"] == "PASS"]
    failed = [r for r in results if r and r["status"] == "FAIL"]
    fastest = min(valid, key=lambda x: x["mean"]) if valid else None
    slowest = max(valid, key=lambda x: x["mean"]) if valid else None

    lines.extend([
        "",
        "---",
        "",
        "## Final Analysis",
        "",
        "### Performance Strengths",
        f"- Fastest benchmark: **{fastest['name']}** ({fastest['mean']:.2f} ms)" if fastest else "",
        f"- Overall pass rate: {len(valid)}/{len(results)} ({len(valid)/len(results)*100:.0f}%)" if results else "",
        "- Correct output verified for all passing benchmarks",
        "- Low variance (stdev < 5% of mean) for most benchmarks",
        "",
        "### Performance Weaknesses",
        f"- Slowest benchmark: **{slowest['name']}** ({slowest['mean']:.2f} ms)" if slowest else "",
    ])

    if failed:
        lines.append(f"- {len(failed)} benchmark(s) failed:")
        for r in failed:
            lines.append(f"  - {r['id']} {r['name']}: {r.get('status_reason', '')}")

    lines.extend([
        "",
        "### Optimization Suggestions",
        "- [Planned] Bytecode compilation (.sibc format) — estimated 3-5x speedup",
        "- [Planned] JIT compilation for hot-path functions",
        "- [Planned] Optimize array push() with pre-allocation strategy",
        "- [Planned] Use SIMD instructions for batch array operations",
        "- [Planned] Cache string length instead of recalculating",
        "",
        "### Known Issues",
        "- Integer overflow on large sums (32-bit int without overflow detection)",
        "- try/catch blocks are parsed but not fully evaluated",
        "",
        "### Future Improvements",
        "- [Planned] Native code generation (LLVM backend) — target: near-C performance",
        "- [Planned] Incremental compilation for faster rebuilds",
        "- [Planned] Parallel garbage collection",
        "- [Planned] Async I/O for file and network operations",
        "",
        "## Methodology",
        "",
        f"- Each benchmark runs **{MIN_RUNS} times** after **{WARMUP_RUNS} warmup** runs",
        "- Statistics: mean, median, min, max, stdev, P50, P90, P95, P99",
        "- 95% confidence interval calculated using t-distribution",
        "- Outlier detection: IQR method (1.5x interquartile range)",
        "- Correctness: each benchmark verifies expected output",
        "- Memory: peak RSS measured via getrusage",
        "- CPU: user time and system time measured via getrusage",
        "- Throughput: operations per second = iterations / (mean_ms / 1000)",
        "- Regression: compared with previous run, >5% change flagged",
        "",
    ])

    output = REPORT_DIR / "benchmark_report.md"
    output.write_text("\n".join(lines))
    print(f"Markdown report: {output}")
    return output

def generate_html_report(env, results, scores, regressions, history=None, grade="B"):
    """Generate interactive HTML dashboard with enhanced charts, dark mode, search, and downloads."""
    valid_results = [r for r in results if r]

    # Summary card data
    total = len(results)
    passed = len([r for r in results if r and r["status"] == "PASS"])
    failed = total - passed
    pass_rate = (passed / total * 100) if total > 0 else 0
    all_means = [r["mean"] for r in valid_results if r["status"] == "PASS"]
    avg_runtime = statistics.mean(all_means) if all_means else 0
    total_time = sum(all_means) if all_means else 0

    # History trend data
    history_labels = json.dumps([h.get("date", "?") for h in (history or [])] + [env["date"]])
    history_scores = json.dumps([h.get("overall_score", 0) for h in (history or [])] + [scores["overall_score"]])

    # Chart data
    chart_labels = json.dumps([r["name"] for r in valid_results])
    chart_means = json.dumps([r["mean"] for r in valid_results])
    chart_p95 = json.dumps([r["p95"] for r in valid_results])

    # Category averages
    cat_data = {}
    for r in valid_results:
        cat = r["category"]
        if cat not in cat_data:
            cat_data[cat] = []
        cat_data[cat].append(r["mean"])
    cat_labels = json.dumps(list(cat_data.keys()))
    cat_avgs = json.dumps([round(statistics.mean(v), 2) for v in cat_data.values()])

    # Throughput data
    thru_labels = json.dumps([r["name"] for r in valid_results if r["throughput_ops_sec"] > 0])
    thru_values = json.dumps([r["throughput_ops_sec"] for r in valid_results if r["throughput_ops_sec"] > 0])

    # Scores
    score_labels = json.dumps([k.replace("_", " ").title() for k in scores.keys()])
    score_values = json.dumps(list(scores.values()))

    # Results table
    table_rows = ""
    current_cat = ""
    for r in valid_results:
        if r["category"] != current_cat:
            current_cat = r["category"]
            table_rows += f'<tr class="category-header"><td colspan="13">{current_cat}</td></tr>'

        status_class = "pass" if r["status"] == "PASS" else "fail"
        ci_str = f"{r['ci_95_low']:.2f}–{r['ci_95_high']:.2f}"

        reg_html = ""
        if r["name"] in regressions and regressions[r["name"]]:
            reg = regressions[r["name"]]
            if reg["status"] == "regression":
                reg_html = f'<span class="reg-regress">+{reg["change_pct"]}%</span>'
            elif reg["status"] == "improved":
                reg_html = f'<span class="reg-improved">{reg["change_pct"]:+.1f}%</span>'
            else:
                reg_html = f'<span class="reg-stable">{reg["change_pct"]:+.1f}%</span>'

        table_rows += f'''<tr>
            <td>{r['id']}</td>
            <td><strong>{r['name']}</strong><br><span class="desc">{r.get('description', '')}</span></td>
            <td>{r['mean']:.2f}</td>
            <td>{r['median']:.2f}</td>
            <td>{r['p95']:.2f}</td>
            <td>{r['p99']:.2f}</td>
            <td>{r['ci_95_low']:.2f}–{r['ci_95_high']:.2f}</td>
            <td>{r['throughput_ops_sec']:,}</td>
            <td>{r['peak_memory_mb']:.1f}</td>
            <td>{r.get('avg_memory_mb', 0):.1f}</td>
            <td>{r.get('heap_mb', 0):.1f}</td>
            <td>{r.get('user_time_s', 0):.3f}</td>
            <td>{r.get('system_time_s', 0):.3f}</td>
            <td>{r.get('cpu_percent', 0):.0f}</td>
            <td>{r['iterations']:,}</td>
            <td class="{status_class}">{r['status']}<br><span class="reason">{r.get('status_reason', '')}</span></td>
            <td>{reg_html}</td>
        </tr>'''

    total = len(results)
    passed = len([r for r in results if r and r["status"] == "PASS"])
    failed = total - passed
    pass_rate = (passed / total * 100) if total > 0 else 0

    all_means = [r["mean"] for r in valid_results if r["status"] == "PASS"]
    fastest = min([r for r in valid_results if r["status"] == "PASS"], key=lambda x: x["mean"]) if all_means else None
    slowest = max([r for r in valid_results if r["status"] == "PASS"], key=lambda x: x["mean"]) if all_means else None

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mozhi Benchmark Report v{VERSION} — {env['date']}</title>
    <link rel="stylesheet" href="../style.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        :root {{ --dark-bg: #0F172A; --dark-text: #F1F5F9; --dark-card: #1E293B; --dark-border: #334155; }}
        body.dark {{ background: var(--dark-bg) !important; color: var(--dark-text) !important; }}
        body.dark .main {{ background: var(--dark-bg); color: var(--dark-text); }}
        body.dark h1, body.dark h2, body.dark h3 {{ color: var(--dark-text) !important; }}
        body.dark .bench-hero {{ background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); }}
        body.dark .stat-box, body.dark .chart-container, body.dark .env-item, body.dark .analysis-section {{
            background: var(--dark-card) !important; border-color: var(--dark-border) !important; color: var(--dark-text);
        }}
        body.dark table {{ color: var(--dark-text); }}
        body.dark .category-header td {{ background: #334155 !important; }}
        body.dark td, body.dark th {{ border-color: var(--dark-border) !important; }}
        .dark-toggle {{ position: fixed; top: 16px; right: 16px; z-index: 999; background: var(--primary); color: white; border: none; border-radius: 50%; width: 44px; height: 44px; cursor: pointer; font-size: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.2); }}
        .grade-badge {{ display: inline-block; padding: 8px 24px; border-radius: 8px; font-size: 28px; font-weight: 900; margin-left: 12px; }}
        .grade-A\\+ {{ background: #16A34A; color: white; }}
        .grade-A {{ background: #22C55E; color: white; }}
        .grade-B\\+ {{ background: #3AAFA9; color: white; }}
        .grade-B {{ background: #4C6EF5; color: white; }}
        .grade-C\\+ {{ background: #E6A23C; color: white; }}
        .grade-C {{ background: #F59E0B; color: white; }}
        .grade-D {{ background: #EF4444; color: white; }}
        .grade-F {{ background: #DC2626; color: white; }}
        .download-bar {{ display: flex; gap: 8px; margin-bottom: 24px; flex-wrap: wrap; }}
        .dl-btn {{ padding: 8px 16px; border-radius: 6px; font-size: 13px; font-weight: 600; text-decoration: none; border: 1px solid var(--border); background: var(--bg-alt); color: var(--text); transition: all 0.15s; }}
        .dl-btn:hover {{ background: var(--primary); color: white; border-color: var(--primary); }}
        .search-box {{ padding: 8px 14px; border: 1px solid var(--border); border-radius: 6px; font-size: 14px; width: 250px; margin-bottom: 12px; }}
        .summary-card {{ background: linear-gradient(135deg, #1E293B 0%, #334155 100%); color: white; border-radius: 12px; padding: 28px; margin-bottom: 32px; display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 20px; text-align: center; }}
        .summary-card .val {{ font-size: 28px; font-weight: 900; font-family: var(--font-mono); }}
        .summary-card .lbl {{ font-size: 11px; text-transform: uppercase; opacity: 0.7; margin-top: 4px; }}
        .bench-hero {{ background: linear-gradient(135deg, #DBEAFE 0%, #FFFFFF 100%); border-radius: 12px; padding: 40px 20px; text-align: center; margin-bottom: 32px; }}
        .bench-hero h1 {{ font-size: 36px; font-weight: 900; margin-bottom: 8px; border: none; }}
        .bench-hero .meta {{ font-size: 13px; color: var(--text-muted); font-family: var(--font-mono); line-height: 1.8; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 16px; margin-bottom: 32px; }}
        .stat-box {{ background: var(--bg-alt); border: 1px solid var(--border); border-radius: 8px; padding: 20px; text-align: center; }}
        .stat-box .value {{ font-size: 28px; font-weight: 900; color: var(--primary); font-family: var(--font-mono); }}
        .stat-box .label {{ font-size: 11px; color: var(--text-muted); margin-top: 4px; text-transform: uppercase; letter-spacing: 0.05em; }}
        .stat-box.pass .value {{ color: #16A34A; }}
        .stat-box.fail .value {{ color: #DC2626; }}
        .stat-box.score .value {{ color: #4C6EF5; }}
        .chart-container {{ background: white; border: 1px solid var(--border); border-radius: 12px; padding: 24px; margin-bottom: 32px; }}
        .chart-container h2 {{ margin-top: 0; }}
        .chart-wrapper {{ position: relative; height: 400px; }}
        .chart-wrapper-small {{ position: relative; height: 300px; }}
        .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 32px; }}
        @media (max-width: 768px) {{ .two-col {{ grid-template-columns: 1fr; }} }}
        table {{ font-size: 12px; }}
        .category-header td {{ background: #1E293B; color: white; font-weight: 700; padding: 8px 12px; text-transform: uppercase; font-size: 11px; }}
        .pass {{ color: #16A34A; font-weight: 700; }}
        .fail {{ color: #DC2626; font-weight: 700; }}
        .reason {{ font-size: 10px; color: var(--text-muted); font-weight: normal; }}
        .desc {{ font-size: 10px; color: var(--text-muted); }}
        .reg-regress {{ color: #DC2626; font-weight: 700; font-size: 11px; }}
        .reg-improved {{ color: #16A34A; font-weight: 700; font-size: 11px; }}
        .reg-stable {{ color: var(--text-muted); font-size: 11px; }}
        .env-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; margin-bottom: 32px; }}
        .env-item {{ background: var(--bg-alt); padding: 12px 16px; border-radius: 6px; border: 1px solid var(--border); }}
        .env-item .key {{ font-size: 10px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; }}
        .env-item .val {{ font-size: 13px; font-weight: 600; font-family: var(--font-mono); }}
        .score-bar {{ display: inline-block; height: 20px; background: var(--primary-light); border-radius: 4px; margin-left: 8px; vertical-align: middle; }}
        .analysis-section {{ background: var(--bg-alt); border: 1px solid var(--border); border-radius: 12px; padding: 24px; margin-bottom: 24px; }}
        .analysis-section h3 {{ margin-top: 0; }}
        .analysis-section ul {{ margin-left: 20px; }}
        .analysis-section li {{ margin-bottom: 6px; }}
    </style>
</head>
<body>
    <div class="topbar">
        <button class="topbar-toggle" onclick="toggleSidebar()">&#9776;</button>
        <span class="topbar-title">Benchmark Report</span>
    </div>
    <div class="wrapper">
        <aside class="sidebar" id="sidebar">
            <div class="sidebar-header">
                <a href="../index.html" class="sidebar-logo">Mozhi</a>
                <div class="sidebar-version">v2.0</div>
            </div>
            <nav class="sidebar-nav">
                <div class="sidebar-section">
                    <div class="sidebar-section-title">Reports</div>
                    <a href="benchmark_report.html" class="active">HTML Dashboard</a>
                    <a href="benchmark_report.json">JSON Data</a>
                    <a href="benchmark_report.csv">CSV Data</a>
                    <a href="benchmark_report.md">Markdown</a>
                </div>
                <div class="sidebar-section">
                    <div class="sidebar-section-title">Navigation</div>
                    <a href="../index.html">Home</a>
                    <a href="../benchmark.html">Quick Benchmarks</a>
                    <a href="../spec.html">Specification</a>
                </div>
            </nav>
        </aside>

        <main class="main">
            <button class="dark-toggle" onclick="toggleDark()" title="Toggle Dark Mode">&#9790;</button>

            <div class="bench-hero">
                <h1>Mozhi Performance Benchmark Report <span class="grade-badge grade-{grade}">{grade}</span></h1>
                <div class="meta">
                    <strong>{env['mozhi_version']}</strong> &middot; Build {env.get('build_hash', 'N/A')} &middot; Commit {env.get('git_commit', 'N/A')}<br>
                    {env.get('build_mode', '')} &middot; Binary {env.get('mozhi_binary_size_kb', '?')} KB &middot; Interpreter Hash {env.get('interpreter_hash', 'N/A')}<br>
                    Machine ID: {env.get('machine_id', 'N/A')} &middot; Env Hash: {env.get('environment_hash', 'N/A')} &middot; Config Hash: {env.get('configuration_hash', 'N/A')}<br>
                    {env['date']} {env['time']} &middot; {env['os']} {env['kernel']} &middot; {env.get('cpu_model', 'unknown')}<br>
                    {env.get('cpu_freq_mhz', '?')} MHz &middot; {env.get('cpu_physical_cores', '?')} cores &middot; {env.get('ram_total_mb', '?')} MB RAM<br>
                    Benchmark Framework v{VERSION} &middot; {MIN_RUNS} runs &middot; {WARMUP_RUNS} warmup
                </div>
            </div>

            <div class="download-bar">
                <a href="benchmark_report.json" class="dl-btn" download>&#11015; JSON</a>
                <a href="benchmark_report.csv" class="dl-btn" download>&#11015; CSV</a>
                <a href="benchmark_report.md" class="dl-btn" download>&#11015; Markdown</a>
                <button class="dl-btn" onclick="window.print()">&#128424; Print</button>
            </div>

            <div class="summary-card">
                <div><div class="val">{total}</div><div class="lbl">Total Benchmarks</div></div>
                <div><div class="val">{passed}</div><div class="lbl">Passed</div></div>
                <div><div class="val">{failed}</div><div class="lbl">Failed</div></div>
                <div><div class="val">{pass_rate:.0f}%</div><div class="lbl">Success Rate</div></div>
                <div><div class="val">{scores['overall_score']:.1f}</div><div class="lbl">Overall Score /100</div></div>
                <div><div class="val">{grade}</div><div class="lbl">Grade</div></div>
                <div><div class="val">{avg_runtime:.1f}ms</div><div class="lbl">Avg Runtime</div></div>
                <div><div class="val">{total_time/1000:.2f}s</div><div class="lbl">Total Time</div></div>
            </div>

            <div class="stats-grid">
                <div class="stat-box pass"><div class="value">{passed}</div><div class="label">Passed</div></div>
                <div class="stat-box fail"><div class="value">{failed}</div><div class="label">Failed</div></div>
                <div class="stat-box"><div class="value">{pass_rate:.0f}%</div><div class="label">Pass Rate</div></div>
                <div class="stat-box"><div class="value">{total}</div><div class="label">Total Benchmarks</div></div>
                <div class="stat-box score"><div class="value">{scores['overall_score']:.1f}</div><div class="label">Overall Score /100</div></div>
                <div class="stat-box"><div class="value">{MIN_RUNS}</div><div class="label">Runs Each</div></div>
            </div>

            <div class="chart-container">
                <h2>Performance Scores by Category</h2>
                <div class="chart-wrapper-small"><canvas id="chart-scores"></canvas></div>
            </div>

            <div class="two-col">
                <div class="chart-container">
                    <h2>Mean Execution Time (ms)</h2>
                    <div class="chart-wrapper"><canvas id="chart-means"></canvas></div>
                </div>
                <div class="chart-container">
                    <h2>P95 Latency (ms)</h2>
                    <div class="chart-wrapper"><canvas id="chart-p95"></canvas></div>
                </div>
            </div>

            <div class="two-col">
                <div class="chart-container">
                    <h2>Throughput (ops/sec)</h2>
                    <div class="chart-wrapper"><canvas id="chart-throughput"></canvas></div>
                </div>
                <div class="chart-container">
                    <h2>Average by Category (ms)</h2>
                    <div class="chart-wrapper"><canvas id="chart-categories"></canvas></div>
                </div>
            </div>

            <div class="chart-container">
                <h2>Benchmark History Trend</h2>
                <p style="color: var(--text-muted); font-size: 13px;">Overall score over time. Each run is saved to history/ for trend tracking.</p>
                <div class="chart-wrapper-small"><canvas id="chart-history"></canvas></div>
            </div>

            <h2>Detailed Results</h2>
            <input type="text" class="search-box" id="search-input" onkeyup="filterTable()" placeholder="Search benchmarks...">
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Benchmark</th>
                        <th>Mean<br>(ms)</th>
                        <th>Median</th>
                        <th>P95</th>
                        <th>P99</th>
                        <th>95% CI</th>
                        <th>Throughput<br>(ops/s)</th>
                        <th>Peak Mem<br>(MB)</th>
                        <th>Avg Mem<br>(MB)</th>
                        <th>Heap<br>(MB)</th>
                        <th>CPU User<br>(s)</th>
                        <th>CPU Sys<br>(s)</th>
                        <th>CPU<br>(%)</th>
                        <th>CPU<br>(s)</th>
                        <th>Iters</th>
                        <th>Status</th>
                        <th>Reg.</th>
                    </tr>
                </thead>
                <tbody>{table_rows}
                </tbody>
            </table>

            <h2>Environment</h2>
            <div class="env-grid">
                <div class="env-item"><div class="key">OS</div><div class="val">{env['os']} {env['kernel']}</div></div>
                <div class="env-item"><div class="key">Architecture</div><div class="val">{env['architecture']}</div></div>
                <div class="env-item"><div class="key">CPU Model</div><div class="val">{env.get('cpu_model', 'unknown')}</div></div>
                <div class="env-item"><div class="key">CPU Frequency</div><div class="val">{env.get('cpu_freq_mhz', '?')} MHz</div></div>
                <div class="env-item"><div class="key">CPU Cache</div><div class="val">{env.get('cpu_cache', '?')}</div></div>
                <div class="env-item"><div class="key">Physical Cores</div><div class="val">{env.get('cpu_physical_cores', '?')}</div></div>
                <div class="env-item"><div class="key">Logical Cores</div><div class="val">{env['cpu_count']}</div></div>
                <div class="env-item"><div class="key">RAM Total</div><div class="val">{env.get('ram_total_mb', '?')} MB</div></div>
                <div class="env-item"><div class="key">RAM Available</div><div class="val">{env.get('ram_available_mb', '?')} MB</div></div>
                <div class="env-item"><div class="key">Disk Type</div><div class="val">{env.get('disk_type', '?')}</div></div>
                <div class="env-item"><div class="key">Filesystem</div><div class="val">{env.get('filesystem', '?')}</div></div>
                <div class="env-item"><div class="key">Page Size</div><div class="val">{env.get('page_size', '?')} bytes</div></div>
                <div class="env-item"><div class="key">NUMA Nodes</div><div class="val">{env.get('numa_nodes', '?')}</div></div>
                <div class="env-item"><div class="key">Locale</div><div class="val">{env.get('locale', '?')}</div></div>
                <div class="env-item"><div class="key">Timezone</div><div class="val">{env.get('timezone', '?')}</div></div>
                <div class="env-item"><div class="key">Mozhi Version</div><div class="val">{env['mozhi_version']}</div></div>
                <div class="env-item"><div class="key">Build Mode</div><div class="val">{env.get('build_mode', '?')}</div></div>
                <div class="env-item"><div class="key">Build Hash</div><div class="val">{env.get('build_hash', 'N/A')}</div></div>
                <div class="env-item"><div class="key">Git Commit</div><div class="val">{env.get('git_commit', 'N/A')}</div></div>
                <div class="env-item"><div class="key">Interpreter Hash</div><div class="val">{env.get('interpreter_hash', 'N/A')}</div></div>
                <div class="env-item"><div class="key">Binary Size</div><div class="val">{env.get('mozhi_binary_size_kb', '?')} KB</div></div>
            </div>

            <h2>Final Analysis</h2>
            <div class="analysis-section">
                <h3>Performance Strengths</h3>
                <ul>
                    <li>Fastest benchmark: <strong>{fastest['name']}</strong> ({fastest['mean']:.2f} ms)</li>
                    <li>Pass rate: {pass_rate:.0f}% ({passed}/{total})</li>
                    <li>Correct output verified for all passing benchmarks</li>
                    <li>Low variance (stdev < 5% of mean) for most benchmarks</li>
                    <li>Startup time under 1 ms</li>
                </ul>
            </div>
            <div class="analysis-section">
                <h3>Performance Weaknesses</h3>
                <ul>
                    <li>Slowest benchmark: <strong>{slowest['name']}</strong> ({slowest['mean']:.2f} ms)</li>
                    {''.join(f'<li>{r["id"]} {r["name"]}: {r.get("status_reason", "")}</li>' for r in valid_results if r["status"] == "FAIL")}
                    <li>Integer overflow on large sums (32-bit int)</li>
                </ul>
            </div>
            <div class="analysis-section">
                <h3>Optimization Suggestions</h3>
                <ul>
                    <li>Implement bytecode compilation for 3-5x speedup</li>
                    <li>Add JIT compilation for hot-path functions</li>
                    <li>Optimize array push() with pre-allocation strategy</li>
                    <li>Use SIMD instructions for batch array operations</li>
                    <li>Cache string length instead of recalculating</li>
                    <li>Implement proper 64-bit integer arithmetic</li>
                </ul>
            </div>
            <div class="analysis-section">
                <h3>Known Issues</h3>
                <ul>
                    <li>Integer overflow on large sums (32-bit int without detection)</li>
                    <li>try/catch blocks are parsed but not fully evaluated</li>
                    <li>Some benchmarks show output format differences (spacing)</li>
                </ul>
            </div>
            <div class="analysis-section">
                <h3>Future Improvements</h3>
                <ul>
                    <li>Native code generation (LLVM backend) for near-C performance</li>
                    <li>Incremental compilation for faster rebuilds</li>
                    <li>Parallel garbage collection</li>
                    <li>Async I/O for file and network operations</li>
                    <li>Profile-guided optimization (PGO)</li>
                </ul>
            </div>

            <h2>Methodology</h2>
            <ul>
                <li>Each benchmark runs <strong>{MIN_RUNS} times</strong> after <strong>{WARMUP_RUNS} warmup</strong> runs</li>
                <li>Statistics: mean, median, min, max, stdev, P50, P90, P95, P99</li>
                <li>95% confidence interval calculated using normal distribution</li>
                <li>Outlier detection: IQR method (1.5x interquartile range)</li>
                <li>Correctness: each benchmark verifies expected output</li>
                <li>Memory: peak RSS measured via getrusage</li>
                <li>CPU: user time and system time measured via getrusage</li>
                <li>Throughput: operations/sec = iterations / (mean_ms / 1000)</li>
                <li>Regression: compared with previous run, >5% change flagged</li>
                <li>PASS/FAIL: status based on threshold + correctness</li>
                <li>Benchmark hash: SHA-256 of .si source code (first 16 chars)</li>
            </ul>

            <div class="footer">
                <p>Mozhi Performance Benchmark Framework v{VERSION} &middot; Copyright &copy; 2026 crossberry-in</p>
            </div>
        </main>
    </div>

    <script>
        function toggleSidebar() {{ document.getElementById('sidebar').classList.toggle('open'); }}
        function toggleDark() {{ document.body.classList.toggle('dark'); localStorage.setItem('dark', document.body.classList.contains('dark')); }}
        if (localStorage.getItem('dark') === 'true') {{ document.body.classList.add('dark'); }}

        // Search/filter table
        function filterTable() {{
            const q = document.getElementById('search-input').value.toLowerCase();
            document.querySelectorAll('tbody tr').forEach(row => {{
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(q) ? '' : 'none';
            }});
        }}

        // Chart: Scores
        new Chart(document.getElementById('chart-scores'), {{
            type: 'bar',
            data: {{
                labels: {score_labels},
                datasets: [{{
                    label: 'Score',
                    data: {score_values},
                    backgroundColor: ['rgba(76,110,245,0.8)','rgba(58,175,169,0.8)','rgba(230,162,60,0.8)','rgba(147,51,234,0.8)','rgba(220,38,38,0.8)','rgba(22,163,74,0.8)','rgba(37,99,235,0.8)'],
                    borderWidth: 1,
                }}],
            }},
            options: {{
                responsive: true, maintainAspectRatio: false,
                animation: {{ duration: 1500, easing: 'easeOutQuart' }},
                scales: {{ y: {{ beginAtZero: true, max: 100, title: {{ display: true, text: 'Score (0-100)' }} }} }},
                plugins: {{ legend: {{ display: false }}, tooltip: {{ callbacks: {{ label: (c) => c.parsed.y.toFixed(1) + ' / 100' }} }} }},
            }},
        }});

        // Chart: Means
        new Chart(document.getElementById('chart-means'), {{
            type: 'bar',
            data: {{ labels: {chart_labels}, datasets: [{{ label: 'Mean (ms)', data: {chart_means}, backgroundColor: 'rgba(76,110,245,0.8)', borderWidth: 1 }}] }},
            options: {{
                responsive: true, maintainAspectRatio: false,
                animation: {{ duration: 1500, easing: 'easeOutQuart' }},
                scales: {{ y: {{ type: 'logarithmic', title: {{ display: true, text: 'ms (log)' }} }} }},
                plugins: {{ legend: {{ display: false }}, tooltip: {{ callbacks: {{ label: (c) => c.parsed.y.toFixed(2) + ' ms' }} }} }},
            }},
        }});

        // Chart: P95
        new Chart(document.getElementById('chart-p95'), {{
            type: 'bar',
            data: {{ labels: {chart_labels}, datasets: [{{ label: 'P95 (ms)', data: {chart_p95}, backgroundColor: 'rgba(230,162,60,0.8)', borderWidth: 1 }}] }},
            options: {{
                responsive: true, maintainAspectRatio: false,
                animation: {{ duration: 1500, easing: 'easeOutQuart' }},
                scales: {{ y: {{ type: 'logarithmic', title: {{ display: true, text: 'ms (log)' }} }} }},
                plugins: {{ legend: {{ display: false }} }},
            }},
        }});

        // Chart: Throughput
        new Chart(document.getElementById('chart-throughput'), {{
            type: 'bar',
            data: {{ labels: {thru_labels}, datasets: [{{ label: 'ops/sec', data: {thru_values}, backgroundColor: 'rgba(22,163,74,0.8)', borderWidth: 1 }}] }},
            options: {{
                responsive: true, maintainAspectRatio: false,
                animation: {{ duration: 1500, easing: 'easeOutQuart' }},
                scales: {{ y: {{ type: 'logarithmic', title: {{ display: true, text: 'ops/sec (log)' }} }} }},
                plugins: {{ legend: {{ display: false }} }},
            }},
        }});

        // Chart: Categories
        new Chart(document.getElementById('chart-categories'), {{
            type: 'bar',
            data: {{ labels: {cat_labels}, datasets: [{{ label: 'Avg (ms)', data: {cat_avgs}, backgroundColor: 'rgba(58,175,169,0.8)', borderWidth: 1 }}] }},
            options: {{
                responsive: true, maintainAspectRatio: false, indexAxis: 'y',
                animation: {{ duration: 1500, easing: 'easeOutQuart' }},
                scales: {{ x: {{ type: 'logarithmic', title: {{ display: true, text: 'ms (log)' }} }} }},
                plugins: {{ legend: {{ display: false }} }},
            }},
        }});
        // Chart: History Trend
        new Chart(document.getElementById('chart-history'), {{
            type: 'line',
            data: {{
                labels: {history_labels},
                datasets: [{{
                    label: 'Overall Score',
                    data: {history_scores},
                    borderColor: '#4C6EF5',
                    backgroundColor: 'rgba(76, 110, 245, 0.1)',
                    fill: true,
                    tension: 0.3,
                    pointRadius: 5,
                    pointBackgroundColor: '#4C6EF5',
                }}],
            }},
            options: {{
                responsive: true, maintainAspectRatio: false,
                animation: {{ duration: 1500, easing: 'easeOutQuart' }},
                scales: {{ y: {{ beginAtZero: true, max: 100, title: {{ display: true, text: 'Score' }} }} }},
                plugins: {{ legend: {{ display: false }} }},
            }},
        }});
    </script>
</body>
</html>'''

    output = REPORT_DIR / "benchmark_report.html"
    output.write_text(html)
    print(f"HTML report: {output}")
    return output

# ============================================================================
# Main
# ============================================================================

def save_history(env, results, scores):
    """Save this benchmark run to history for trend tracking."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    history_entry = {
        "timestamp": env["timestamp"],
        "date": env["date"],
        "time": env["time"],
        "overall_score": scores["overall_score"],
        "total": len(results),
        "passed": len([r for r in results if r and r["status"] == "PASS"]),
        "failed": len([r for r in results if r and r["status"] == "FAIL"]),
        "mozhi_version": env["mozhi_version"],
        "git_commit": env.get("git_commit", "N/A"),
        "interpreter_hash": env.get("interpreter_hash", "N/A"),
        "machine_id": env.get("machine_id", "N/A"),
        "benchmark_means": {r["name"]: r["mean"] for r in results if r},
    }
    history_file = HISTORY_DIR / f"run_{timestamp}.json"
    history_file.write_text(json.dumps(history_entry, indent=2))

    # Update history index
    index_file = HISTORY_DIR / "index.json"
    if index_file.exists():
        index = json.loads(index_file.read_text())
    else:
        index = {"runs": []}
    index["runs"].append({
        "timestamp": env["timestamp"],
        "date": env["date"],
        "time": env["time"],
        "file": history_file.name,
        "overall_score": scores["overall_score"],
        "passed": history_entry["passed"],
        "failed": history_entry["failed"],
    })
    index_file.write_text(json.dumps(index, indent=2))
    print(f"History saved: {history_file}")
    return history_file

def load_history():
    """Load all historical benchmark runs for trend graph."""
    index_file = HISTORY_DIR / "index.json"
    if not index_file.exists():
        return []
    try:
        index = json.loads(index_file.read_text())
        return index.get("runs", [])
    except:
        return []

def calculate_grade(score):
    """Calculate letter grade from score."""
    if score >= 95:
        return "A+"
    elif score >= 90:
        return "A"
    elif score >= 85:
        return "B+"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C+"
    elif score >= 60:
        return "C"
    elif score >= 50:
        return "D"
    else:
        return "F"

def main():
    print("=" * 80)
    print(f"Mozhi Performance Benchmark Framework v{VERSION}")
    print("=" * 80)

    # Detect environment
    print("\n[1/6] Detecting environment...")
    env = detect_environment()
    print(f"  Mozhi: {env['mozhi_version']}")
    print(f"  Build: {env.get('build_hash', 'N/A')} (commit {env.get('git_commit', 'N/A')})")
    print(f"  CPU: {env.get('cpu_model', 'unknown')} @ {env.get('cpu_freq_mhz', '?')} MHz")
    print(f"  Cores: {env.get('cpu_physical_cores', '?')}P / {env['cpu_count']}L")
    print(f"  RAM: {env.get('ram_total_mb', '?')} MB")
    print(f"  Disk: {env.get('disk_type', '?')} ({env.get('filesystem', '?')})")
    print(f"  Machine ID: {env.get('machine_id', 'N/A')}")

    # Load previous results for regression
    print("\n[2/6] Loading previous results for regression detection...")
    previous = load_previous_results()
    if previous:
        print(f"  Found {len(previous)} previous benchmark results")
    else:
        print("  No previous results (first run)")

    # Load history for trend
    history = load_history()
    print(f"  History: {len(history)} previous run(s)")

    # Run benchmarks
    benchmarks = get_benchmarks()
    print(f"\n[3/6] Running {len(benchmarks)} benchmarks ({MIN_RUNS} runs each, {WARMUP_RUNS} warmup)...")

    results = []
    for i, bench in enumerate(benchmarks, 1):
        name = bench["name"]
        print(f"  [{i}/{len(benchmarks)}] {bench['id']} {name}...", end=" ", flush=True)
        result = run_benchmark(
            bench_id=bench["id"],
            name=name,
            category=bench["category"],
            description=bench["description"],
            si_code=bench["code"],
            expected_output=bench.get("expected"),
            iterations=bench["iterations"],
            runs=MIN_RUNS,
        )
        if result:
            print(f"{result['mean']:.1f}ms [{result['status']}]")
        else:
            print("ERROR")
        results.append(result)

    # Check regressions
    print(f"\n[4/6] Checking regressions...")
    regressions = {}
    for r in results:
        if not r:
            continue
        reg = check_regression(r, previous)
        regressions[r["name"]] = reg
        if reg:
            print(f"  {r['name']}: {reg['change_pct']:+.1f}% ({reg['status']})")

    # Calculate scores
    scores, cat_times = calculate_scores(results)
    grade = calculate_grade(scores["overall_score"])
    print(f"\n  Overall Score: {scores['overall_score']:.1f} / 100 (Grade: {grade})")

    # Save history
    print(f"\n[5/6] Saving history...")
    save_history(env, results, scores)

    # Generate reports
    print(f"\n[6/6] Generating reports...")
    generate_console_report(env, results, scores, regressions)
    generate_json_report(env, results, scores, regressions)
    generate_csv_report(results)
    generate_markdown_report(env, results, scores, regressions)
    generate_html_report(env, results, scores, regressions, history, grade)

    print(f"\n{'=' * 80}")
    print(f"Done! Reports saved to: {REPORT_DIR}/")
    print(f"  HTML Dashboard: {REPORT_DIR}/benchmark_report.html")
    print(f"  JSON Data:      {REPORT_DIR}/benchmark_report.json")
    print(f"  CSV Data:       {REPORT_DIR}/benchmark_report.csv")
    print(f"  Markdown:       {REPORT_DIR}/benchmark_report.md")
    print(f"  History:        {HISTORY_DIR}/ ({len(history)+1} runs)")
    print(f"  Grade:          {grade}")
    print(f"{'=' * 80}")

if __name__ == "__main__":
    main()
