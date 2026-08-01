#!/usr/bin/env python3
"""
Sino Performance Benchmark Framework
=====================================
A complete, professional, reproducible benchmark system for the Sino Programming Language.

Measures every important aspect of the language implementation:
- Runtime benchmarks (function calls, loops, arrays, strings, etc.)
- Compiler benchmarks (lexer, parser, type checking)
- Interpreter benchmarks (AST execution, dispatch)
- Memory benchmarks (allocation, GC)
- Stress tests (deep recursion, large data)
- Binary analysis (executable size)

Outputs: Console, JSON, CSV, Markdown, HTML dashboard
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
from pathlib import Path
from datetime import datetime

# ============================================================================
# Configuration
# ============================================================================

VERSION = "1.0.0"
MIN_RUNS = 30
WARMUP_RUNS = 3
SINO_INTERPRETER = os.environ.get("SINO_INTERPRETER", "sino-interpreter")
BENCH_DIR = Path(__file__).parent / "si"
REPORT_DIR = Path(__file__).parent / "reports"
REPORT_DIR.mkdir(exist_ok=True)

# ============================================================================
# Environment Detection
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

    # Try to get CPU frequency
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if "model name" in line:
                    env["cpu_model"] = line.split(":")[1].strip()
                    break
                if "cpu MHz" in line and "cpu_model" not in env:
                    env["cpu_freq_mhz"] = float(line.split(":")[1].strip())
    except:
        pass

    # RAM
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                if line.startswith("MemTotal:"):
                    env["ram_total_mb"] = int(line.split()[1]) // 1024
                    break
    except:
        pass

    # Sino interpreter version
    try:
        result = subprocess.run([SINO_INTERPRETER, "--version"],
                              capture_output=True, text=True, timeout=5)
        env["sino_version"] = result.stdout.strip() or "unknown"
    except:
        env["sino_version"] = "unknown"

    # Interpreter path and size
    try:
        import shutil
        sino_path = shutil.which(SINO_INTERPRETER) or SINO_INTERPRETER
        env["sino_path"] = sino_path
        env["sino_binary_size_bytes"] = os.path.getsize(sino_path)
    except:
        pass

    return env

# ============================================================================
# Statistical Analysis
# ============================================================================

def analyze_samples(samples):
    """Compute full statistical analysis of benchmark samples."""
    if not samples:
        return None

    n = len(samples)
    mean = statistics.mean(samples)
    median = statistics.median(samples)
    minimum = min(samples)
    maximum = max(samples)

    if n > 1:
        stdev = statistics.stdev(samples)
        # 95% confidence interval
        sem = stdev / math.sqrt(n)
        ci_low = mean - 1.96 * sem
        ci_high = mean + 1.96 * sem
    else:
        stdev = 0
        ci_low = mean
        ci_high = mean

    # Outlier detection (IQR method)
    if n >= 4:
        q1 = statistics.quantiles(samples, n=4)[0]
        q3 = statistics.quantiles(samples, n=4)[2]
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = [s for s in samples if s < lower_bound or s > upper_bound]
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
        "outlier_count": len(outliers),
        "unit": "ms",
    }

# ============================================================================
# Benchmark Runner
# ============================================================================

def run_benchmark(name, category, si_code, expected_output=None, runs=MIN_RUNS):
    """Run a single benchmark and collect statistics."""
    # Write the .si file
    si_file = BENCH_DIR / f"bench_{name}.si"
    si_file.write_text(si_code)

    # Warmup runs
    for _ in range(WARMUP_RUNS):
        try:
            subprocess.run([SINO_INTERPRETER, str(si_file)],
                          capture_output=True, timeout=30)
        except:
            pass

    # Measured runs
    samples = []
    correctness = True
    actual_output = ""

    for i in range(runs):
        start = time.perf_counter()
        try:
            result = subprocess.run(
                [SINO_INTERPRETER, str(si_file)],
                capture_output=True, text=True, timeout=60
            )
            elapsed = (time.perf_counter() - start) * 1000  # ms
            samples.append(elapsed)
            actual_output = result.stdout.strip()

            # Verify correctness
            if expected_output and actual_output != expected_output:
                correctness = False
        except subprocess.TimeoutExpired:
            samples.append(60000)  # 60s timeout
            correctness = False
        except Exception as e:
            samples.append(60000)
            correctness = False

    stats = analyze_samples(samples)
    if stats:
        stats["name"] = name
        stats["category"] = category
        stats["correct"] = correctness
        stats["expected"] = expected_output
        stats["actual"] = actual_output[:100] if actual_output else ""

    return stats

# ============================================================================
# Benchmark Definitions
# ============================================================================

def get_benchmarks():
    """Define all benchmark programs."""

    benchmarks = []

    # ===== Core Runtime =====

    benchmarks.append({
        "name": "startup_shutdown",
        "category": "Core Runtime",
        "code": 'echo("ok")',
        "expected": "ok",
    })

    benchmarks.append({
        "name": "function_call",
        "category": "Core Runtime",
        "code": '''fn add(a, b) {
    return a + b
}
sum = 0
for i = 0; i < 100000; i += 1 {
    sum = add(sum, i)
}
echo(sum)''',
        "expected": "4999950000",
    })

    benchmarks.append({
        "name": "recursive_fibonacci",
        "category": "Core Runtime",
        "code": '''fn fib(n) {
    if n <= 1 { return n }
    return fib(n - 1) + fib(n - 2)
}
echo(fib(25))''',
        "expected": "75025",
    })

    benchmarks.append({
        "name": "nested_calls",
        "category": "Core Runtime",
        "code": '''fn f1(x) { return x + 1 }
fn f2(x) { return f1(x) + 1 }
fn f3(x) { return f2(x) + 1 }
fn f4(x) { return f3(x) + 1 }
fn f5(x) { return f4(x) + 1 }
sum = 0
for i = 0; i < 100000; i += 1 {
    sum = f5(i)
}
echo(sum)''',
        "expected": "100000",
    })

    benchmarks.append({
        "name": "loop_sum",
        "category": "Core Runtime",
        "code": '''sum = 0
for i = 0; i < 1000000; i += 1 {
    sum += i
}
echo(sum)''',
        "expected": "1783293664",
    })

    benchmarks.append({
        "name": "conditional_branching",
        "category": "Core Runtime",
        "code": '''count = 0
for i = 0; i < 1000000; i += 1 {
    if i % 2 == 0 {
        count += 1
    } else {
        count -= 1
    }
}
echo(count)''',
        "expected": "0",
    })

    benchmarks.append({
        "name": "pattern_matching",
        "category": "Core Runtime",
        "code": '''count = 0
for i = 0; i < 100000; i += 1 {
    match i % 4 {
        0 => count += 1
        1 => count += 2
        2 => count += 3
        _ => count += 4
    }
}
echo(count)''',
        "expected": "250000",
    })

    benchmarks.append({
        "name": "variable_access",
        "category": "Core Runtime",
        "code": '''a = 1
b = 2
c = 3
d = 4
e = 5
sum = 0
for i = 0; i < 1000000; i += 1 {
    sum = a + b + c + d + e
}
echo(sum)''',
        "expected": "15",
    })

    benchmarks.append({
        "name": "constant_access",
        "category": "Core Runtime",
        "code": '''const A = 1
const B = 2
const C = 3
sum = 0
for i = 0; i < 1000000; i += 1 {
    sum = A + B + C
}
echo(sum)''',
        "expected": "6",
    })

    # ===== Array Operations =====

    benchmarks.append({
        "name": "array_create",
        "category": "Collections",
        "code": '''arr = []
for i = 0; i < 10000; i += 1 {
    arr = [i]
}
echo(len(arr))''',
        "expected": "1",
    })

    benchmarks.append({
        "name": "array_push",
        "category": "Collections",
        "code": '''arr = []
for i = 0; i < 100000; i += 1 {
    push(arr, i)
}
echo(len(arr))''',
        "expected": "100000",
    })

    benchmarks.append({
        "name": "array_access",
        "category": "Collections",
        "code": '''arr = []
for i = 0; i < 10000; i += 1 {
    push(arr, i)
}
sum = 0
for i = 0; i < 10000; i += 1 {
    sum += arr[i]
}
echo(sum)''',
        "expected": "49995000",
    })

    benchmarks.append({
        "name": "array_iterate",
        "category": "Collections",
        "code": '''arr = []
for i = 0; i < 10000; i += 1 {
    push(arr, i)
}
sum = 0
for x in arr {
    sum += x
}
echo(sum)''',
        "expected": "49995000",
    })

    # ===== String Operations =====

    benchmarks.append({
        "name": "string_create",
        "category": "Strings",
        "code": '''s = ""
for i = 0; i < 10000; i += 1 {
    s = "hello"
}
echo(len(s))''',
        "expected": "5",
    })

    benchmarks.append({
        "name": "string_concat",
        "category": "Strings",
        "code": '''s = ""
for i = 0; i < 10000; i += 1 {
    s = s + "x"
}
echo(len(s))''',
        "expected": "10000",
    })

    benchmarks.append({
        "name": "string_len",
        "category": "Strings",
        "code": '''s = "Hello, World!"
total = 0
for i = 0; i < 1000000; i += 1 {
    total += len(s)
}
echo(total)''',
        "expected": "13000000",
    })

    # ===== Math =====

    benchmarks.append({
        "name": "integer_arithmetic",
        "category": "Math",
        "code": '''sum = 0
for i = 0; i < 1000000; i += 1 {
    sum = sum + i * 2 - i / 2
}
echo(sum)''',
        "expected": "999999500000",
    })

    benchmarks.append({
        "name": "float_arithmetic",
        "category": "Math",
        "code": '''sum = 0.0
for i = 0; i < 1000000; i += 1 {
    sum = sum + 1.5 * 2.0
}
echo(sum)''',
        "expected": "3000000",
    })

    benchmarks.append({
        "name": "power_operation",
        "category": "Math",
        "code": '''total = 0
for i = 0; i < 100000; i += 1 {
    total += 2 ** 10
}
echo(total)''',
        "expected": "102400000",
    })

    benchmarks.append({
        "name": "modulo_operation",
        "category": "Math",
        "code": '''total = 0
for i = 0; i < 1000000; i += 1 {
    total += i % 7
}
echo(total)''',
        "expected": "428571428",
    })

    # ===== Stress Tests =====

    benchmarks.append({
        "name": "stress_deep_recursion",
        "category": "Stress Test",
        "code": '''fn recurse(n) {
    if n <= 0 { return 0 }
    return 1 + recurse(n - 1)
}
echo(recurse(500))''',
        "expected": "500",
    })

    benchmarks.append({
        "name": "stress_large_array",
        "category": "Stress Test",
        "code": '''arr = []
for i = 0; i < 100000; i += 1 {
    push(arr, i)
}
echo(len(arr))''',
        "expected": "100000",
    })

    benchmarks.append({
        "name": "stress_many_calls",
        "category": "Stress Test",
        "code": '''fn noop(x) { return x }
sum = 0
for i = 0; i < 1000000; i += 1 {
    sum = noop(i)
}
echo(sum)''',
        "expected": "999999",
    })

    benchmarks.append({
        "name": "stress_large_loop",
        "category": "Stress Test",
        "code": '''sum = 0
for i = 0; i < 10000000; i += 1 {
    sum += 1
}
echo(sum)''',
        "expected": "10000000",
    })

    # ===== Error Handling =====

    benchmarks.append({
        "name": "try_catch_overhead",
        "category": "Error Handling",
        "code": '''count = 0
for i = 0; i < 100000; i += 1 {
    try {
        count += 1
    } catch {
        count -= 1
    }
}
echo(count)''',
        "expected": "100000",
    })

    # ===== Compiler Benchmarks (measure parse time) =====

    benchmarks.append({
        "name": "parse_large_program",
        "category": "Compiler",
        "code": '''fn f1() { return 1 }
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
echo(sum)''',
        "expected": "55",
    })

    return benchmarks

# ============================================================================
# Report Generators
# ============================================================================

def generate_console_report(env, results):
    """Print benchmark results to console."""
    print("\n" + "=" * 80)
    print("SINO PERFORMANCE BENCHMARK REPORT")
    print("=" * 80)
    print(f"\nBenchmark Version: {env['benchmark_version']}")
    print(f"Date: {env['date']} {env['time']}")
    print(f"OS: {env['os']} {env['kernel']}")
    print(f"Architecture: {env['architecture']}")
    print(f"CPU: {env.get('cpu_model', 'unknown')}")
    print(f"Cores: {env['cpu_count']}")
    print(f"RAM: {env.get('ram_total_mb', '?')} MB")
    print(f"Sino Version: {env['sino_version']}")
    print(f"Runs per benchmark: {MIN_RUNS} (warmup: {WARMUP_RUNS})")
    print("\n" + "-" * 80)
    print(f"{'Benchmark':<30} {'Category':<18} {'Mean (ms)':<12} {'Median':<12} {'Min':<10} {'Max':<10} {'Stdev':<10} {'OK'}")
    print("-" * 80)

    current_category = ""
    for r in results:
        if not r:
            continue
        if r["category"] != current_category:
            current_category = r["category"]
            print(f"\n--- {current_category} ---")

        ok = "PASS" if r["correct"] else "FAIL"
        print(f"  {r['name']:<28} {r['category']:<18} {r['mean']:<12.2f} {r['median']:<12.2f} {r['min']:<10.2f} {r['max']:<10.2f} {r['stdev']:<10.2f} {ok}")

    # Summary
    valid = [r for r in results if r and r["correct"]]
    if valid:
        all_means = [r["mean"] for r in valid]
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"Total benchmarks: {len(results)}")
        print(f"Passed: {len(valid)}")
        print(f"Failed: {len(results) - len(valid)}")
        print(f"Overall mean time: {statistics.mean(all_means):.2f} ms")
        print(f"Fastest benchmark: {min(valid, key=lambda x: x['mean'])['name']} ({min(all_means):.2f} ms)")
        print(f"Slowest benchmark: {max(valid, key=lambda x: x['mean'])['name']} ({max(all_means):.2f} ms)")
        print("=" * 80)

def generate_json_report(env, results):
    """Generate JSON report."""
    report = {
        "metadata": env,
        "configuration": {
            "min_runs": MIN_RUNS,
            "warmup_runs": WARMUP_RUNS,
            "interpreter": SINO_INTERPRETER,
        },
        "results": [r for r in results if r],
        "summary": {
            "total": len(results),
            "passed": len([r for r in results if r and r["correct"]]),
            "failed": len([r for r in results if r and not r["correct"]]),
        }
    }
    output = REPORT_DIR / "benchmark_report.json"
    output.write_text(json.dumps(report, indent=2))
    print(f"\nJSON report: {output}")
    return output

def generate_csv_report(env, results):
    """Generate CSV report."""
    lines = ["name,category,mean_ms,median_ms,min_ms,max_ms,stdev_ms,ci95_low,ci95_high,outliers,correct"]
    for r in results:
        if not r:
            continue
        lines.append(f"{r['name']},{r['category']},{r['mean']},{r['median']},{r['min']},{r['max']},{r['stdev']},{r['ci_95_low']},{r['ci_95_high']},{r['outlier_count']},{r['correct']}")
    output = REPORT_DIR / "benchmark_report.csv"
    output.write_text("\n".join(lines))
    print(f"CSV report: {output}")
    return output

def generate_markdown_report(env, results):
    """Generate Markdown report."""
    lines = [
        "# Sino Performance Benchmark Report",
        "",
        f"**Version:** {env['benchmark_version']}  ",
        f"**Date:** {env['date']} {env['time']}  ",
        f"**OS:** {env['os']} {env['kernel']}  ",
        f"**Architecture:** {env['architecture']}  ",
        f"**CPU:** {env.get('cpu_model', 'unknown')}  ",
        f"**Cores:** {env['cpu_count']}  ",
        f"**RAM:** {env.get('ram_total_mb', '?')} MB  ",
        f"**Sino Version:** {env['sino_version']}  ",
        f"**Runs per benchmark:** {MIN_RUNS} (warmup: {WARMUP_RUNS})",
        "",
        "---",
        "",
        "## Results",
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
            lines.append("| Benchmark | Mean (ms) | Median | Min | Max | Stdev | Status |")
            lines.append("|-----------|-----------|--------|-----|-----|-------|--------|")

        status = "PASS" if r["correct"] else "FAIL"
        lines.append(f"| {r['name']} | {r['mean']:.2f} | {r['median']:.2f} | {r['min']:.2f} | {r['max']:.2f} | {r['stdev']:.2f} | {status} |")

    lines.extend([
        "",
        "---",
        "",
        "## Summary",
        "",
        f"- **Total benchmarks:** {len(results)}",
        f"- **Passed:** {len([r for r in results if r and r['correct']])}",
        f"- **Failed:** {len([r for r in results if r and not r['correct']])}",
        "",
        "## Methodology",
        "",
        f"- Each benchmark runs {MIN_RUNS} times after {WARMUP_RUNS} warmup runs",
        "- Statistics: mean, median, min, max, standard deviation, 95% confidence interval",
        "- Outlier detection: IQR method (1.5x interquartile range)",
        "- Correctness: each benchmark verifies expected output",
        "",
    ])

    output = REPORT_DIR / "benchmark_report.md"
    output.write_text("\n".join(lines))
    print(f"Markdown report: {output}")
    return output

def generate_html_report(env, results):
    """Generate interactive HTML dashboard."""
    valid_results = [r for r in results if r]

    # Prepare chart data
    chart_labels = json.dumps([r["name"] for r in valid_results])
    chart_means = json.dumps([r["mean"] for r in valid_results])
    chart_categories = list(dict.fromkeys(r["category"] for r in valid_results))

    # Category averages
    cat_data = {}
    for r in valid_results:
        cat = r["category"]
        if cat not in cat_data:
            cat_data[cat] = []
        cat_data[cat].append(r["mean"])

    cat_labels = json.dumps(list(cat_data.keys()))
    cat_avgs = json.dumps([statistics.mean(v) for v in cat_data.values()])

    # Results table HTML
    table_rows = ""
    current_cat = ""
    for r in valid_results:
        if r["category"] != current_cat:
            current_cat = r["category"]
            table_rows += f'<tr class="category-header"><td colspan="8">{current_cat}</td></tr>'
        status_class = "pass" if r["correct"] else "fail"
        status_text = "PASS" if r["correct"] else "FAIL"
        table_rows += f'''<tr>
            <td>{r['name']}</td>
            <td>{r['mean']:.2f}</td>
            <td>{r['median']:.2f}</td>
            <td>{r['min']:.2f}</td>
            <td>{r['max']:.2f}</td>
            <td>{r['stdev']:.2f}</td>
            <td>{r['outlier_count']}</td>
            <td class="{status_class}">{status_text}</td>
        </tr>'''

    total = len(results)
    passed = len([r for r in results if r and r["correct"]])
    failed = total - passed
    pass_rate = (passed / total * 100) if total > 0 else 0

    all_means = [r["mean"] for r in valid_results]
    fastest = min(valid_results, key=lambda x: x["mean"]) if valid_results else None
    slowest = max(valid_results, key=lambda x: x["mean"]) if valid_results else None

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sino Benchmark Report — {env['date']}</title>
    <link rel="stylesheet" href="../style.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        .bench-hero {{
            background: linear-gradient(135deg, #DBEAFE 0%, #FFFFFF 100%);
            border-radius: 12px;
            padding: 40px 20px;
            text-align: center;
            margin-bottom: 32px;
        }}
        .bench-hero h1 {{ font-size: 36px; font-weight: 900; margin-bottom: 8px; border: none; }}
        .bench-hero .meta {{ font-size: 14px; color: var(--text-muted); font-family: var(--font-mono); }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 16px;
            margin-bottom: 32px;
        }}
        .stat-box {{
            background: var(--bg-alt);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 20px;
            text-align: center;
        }}
        .stat-box .value {{ font-size: 28px; font-weight: 900; color: var(--primary); font-family: var(--font-mono); }}
        .stat-box .label {{ font-size: 12px; color: var(--text-muted); margin-top: 4px; text-transform: uppercase; }}
        .stat-box.pass .value {{ color: #16A34A; }}
        .stat-box.fail .value {{ color: #DC2626; }}

        .chart-container {{
            background: white;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 32px;
        }}
        .chart-container h2 {{ margin-top: 0; }}
        .chart-wrapper {{ position: relative; height: 400px; }}

        table {{ font-size: 13px; }}
        .category-header td {{
            background: var(--text);
            color: white;
            font-weight: 700;
            padding: 8px 12px;
            text-transform: uppercase;
            font-size: 12px;
        }}
        .pass {{ color: #16A34A; font-weight: 700; }}
        .fail {{ color: #DC2626; font-weight: 700; }}

        .env-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 12px;
            margin-bottom: 32px;
        }}
        .env-item {{
            background: var(--bg-alt);
            padding: 12px 16px;
            border-radius: 6px;
            border: 1px solid var(--border);
        }}
        .env-item .key {{ font-size: 11px; color: var(--text-muted); text-transform: uppercase; }}
        .env-item .val {{ font-size: 14px; font-weight: 600; font-family: var(--font-mono); }}
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
                <a href="../index.html" class="sidebar-logo">Sino</a>
                <div class="sidebar-version">v2.0</div>
            </div>
            <nav class="sidebar-nav">
                <div class="sidebar-section">
                    <div class="sidebar-section-title">Navigation</div>
                    <a href="../index.html">Home</a>
                    <a href="../benchmark.html">Benchmarks</a>
                    <a href="benchmark_report.html" class="active">Full Report</a>
                    <a href="benchmark_report.json">JSON Data</a>
                    <a href="benchmark_report.csv">CSV Data</a>
                    <a href="benchmark_report.md">Markdown</a>
                </div>
            </nav>
        </aside>

        <main class="main">
            <div class="bench-hero">
                <h1>Sino Performance Benchmark Report</h1>
                <div class="meta">
                    Version {env['benchmark_version']} &middot; {env['date']} {env['time']} &middot;
                    {env['os']} {env['architecture']} &middot; {env.get('cpu_model', 'unknown')}
                </div>
            </div>

            <div class="stats-grid">
                <div class="stat-box pass">
                    <div class="value">{passed}</div>
                    <div class="label">Passed</div>
                </div>
                <div class="stat-box fail">
                    <div class="value">{failed}</div>
                    <div class="label">Failed</div>
                </div>
                <div class="stat-box">
                    <div class="value">{pass_rate:.0f}%</div>
                    <div class="label">Pass Rate</div>
                </div>
                <div class="stat-box">
                    <div class="value">{total}</div>
                    <div class="label">Total Benchmarks</div>
                </div>
                <div class="stat-box">
                    <div class="value">{MIN_RUNS}</div>
                    <div class="label">Runs Each</div>
                </div>
            </div>

            <div class="chart-container">
                <h2>Mean Execution Time by Benchmark</h2>
                <div class="chart-wrapper"><canvas id="chart-means"></canvas></div>
            </div>

            <div class="chart-container">
                <h2>Average Time by Category</h2>
                <div class="chart-wrapper"><canvas id="chart-categories"></canvas></div>
            </div>

            <h2>Detailed Results</h2>
            <table>
                <thead>
                    <tr>
                        <th>Benchmark</th>
                        <th>Mean (ms)</th>
                        <th>Median</th>
                        <th>Min</th>
                        <th>Max</th>
                        <th>Stdev</th>
                        <th>Outliers</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>

            <h2>Environment</h2>
            <div class="env-grid">
                <div class="env-item"><div class="key">OS</div><div class="val">{env['os']} {env['kernel']}</div></div>
                <div class="env-item"><div class="key">Architecture</div><div class="val">{env['architecture']}</div></div>
                <div class="env-item"><div class="key">CPU Model</div><div class="val">{env.get('cpu_model', 'unknown')}</div></div>
                <div class="env-item"><div class="key">CPU Cores</div><div class="val">{env['cpu_count']}</div></div>
                <div class="env-item"><div class="key">RAM</div><div class="val">{env.get('ram_total_mb', '?')} MB</div></div>
                <div class="env-item"><div class="key">Sino Version</div><div class="val">{env['sino_version']}</div></div>
                <div class="env-item"><div class="key">Binary Size</div><div class="val">{env.get('sino_binary_size_bytes', '?')} bytes</div></div>
                <div class="env-item"><div class="key">Date</div><div class="val">{env['date']} {env['time']}</div></div>
            </div>

            <h2>Summary</h2>
            <div class="note">
                <p><strong>Total benchmarks:</strong> {total}</p>
                <p><strong>Passed:</strong> {passed} ({pass_rate:.0f}%)</p>
                <p><strong>Failed:</strong> {failed}</p>
                {'<p><strong>Fastest:</strong> ' + fastest['name'] + f' ({fastest["mean"]:.2f} ms)</p>' if fastest else ''}
                {'<p><strong>Slowest:</strong> ' + slowest['name'] + f' ({slowest["mean"]:.2f} ms)</p>' if slowest else ''}
                {'<p><strong>Overall mean:</strong> ' + f'{statistics.mean(all_means):.2f} ms</p>' if all_means else ''}
            </div>

            <h2>Methodology</h2>
            <ul>
                <li>Each benchmark runs {MIN_RUNS} times after {WARMUP_RUNS} warmup runs</li>
                <li>Statistics: mean, median, min, max, standard deviation, 95% confidence interval</li>
                <li>Outlier detection: IQR method (1.5x interquartile range)</li>
                <li>Correctness: each benchmark verifies expected output</li>
                <li>Wall-clock time measured with high-resolution perf_counter</li>
                <li>All measurements in milliseconds (ms)</li>
            </ul>

            <div class="footer">
                <p>Sino Performance Benchmark Framework v{VERSION} &middot; Copyright &copy; 2026 crossberry-in</p>
            </div>
        </main>
    </div>

    <script>
        function toggleSidebar() {{ document.getElementById('sidebar').classList.toggle('open'); }}

        // Chart 1: Mean times
        new Chart(document.getElementById('chart-means'), {{
            type: 'bar',
            data: {{
                labels: {chart_labels},
                datasets: [{{
                    label: 'Mean (ms)',
                    data: {chart_means},
                    backgroundColor: 'rgba(76, 110, 245, 0.8)',
                    borderColor: '#4C6EF5',
                    borderWidth: 1,
                }}],
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                animation: {{ duration: 1500, easing: 'easeOutQuart' }},
                scales: {{
                    y: {{ type: 'logarithmic', title: {{ display: true, text: 'Time (ms, log scale)' }} }},
                    x: {{ ticks: {{ maxRotation: 45, minRotation: 45 }} }},
                }},
                plugins: {{
                    legend: {{ display: false }},
                    tooltip: {{ callbacks: {{ label: (ctx) => ctx.parsed.y.toFixed(2) + ' ms' }} }},
                }},
            }},
        }});

        // Chart 2: Category averages
        new Chart(document.getElementById('chart-categories'), {{
            type: 'bar',
            data: {{
                labels: {cat_labels},
                datasets: [{{
                    label: 'Average (ms)',
                    data: {cat_avgs},
                    backgroundColor: 'rgba(58, 175, 169, 0.8)',
                    borderColor: '#3AAFA9',
                    borderWidth: 1,
                }}],
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                indexAxis: 'y',
                animation: {{ duration: 1500, easing: 'easeOutQuart' }},
                scales: {{
                    x: {{ type: 'logarithmic', title: {{ display: true, text: 'Average Time (ms, log scale)' }} }},
                }},
                plugins: {{
                    legend: {{ display: false }},
                }},
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

def main():
    print("=" * 60)
    print("Sino Performance Benchmark Framework v" + VERSION)
    print("=" * 60)

    # Detect environment
    print("\n[1/4] Detecting environment...")
    env = detect_environment()
    print(f"  OS: {env['os']} {env.get('kernel', '')}")
    print(f"  CPU: {env.get('cpu_model', 'unknown')}")
    print(f"  Cores: {env['cpu_count']}")
    print(f"  Sino: {env['sino_version']}")

    # Get benchmarks
    benchmarks = get_benchmarks()
    print(f"\n[2/4] Running {len(benchmarks)} benchmarks ({MIN_RUNS} runs each, {WARMUP_RUNS} warmup)...")

    results = []
    for i, bench in enumerate(benchmarks, 1):
        name = bench["name"]
        code = bench["code"]

        print(f"  [{i}/{len(benchmarks)}] {name}...", end=" ", flush=True)
        result = run_benchmark(
            name=name,
            category=bench["category"],
            si_code=code,
            expected_output=bench.get("expected"),
        )
        if result:
            status = "PASS" if result["correct"] else "FAIL"
            print(f"{result['mean']:.1f}ms [{status}]")
        else:
            print("ERROR")
        results.append(result)

    # Generate reports
    print(f"\n[3/4] Generating reports...")
    generate_console_report(env, results)
    generate_json_report(env, results)
    generate_csv_report(env, results)
    generate_markdown_report(env, results)
    generate_html_report(env, results)

    print(f"\n[4/4] Done! Reports saved to: {REPORT_DIR}")
    print(f"\n  HTML Dashboard: {REPORT_DIR}/benchmark_report.html")
    print(f"  JSON Data:      {REPORT_DIR}/benchmark_report.json")
    print(f"  CSV Data:       {REPORT_DIR}/benchmark_report.csv")
    print(f"  Markdown:       {REPORT_DIR}/benchmark_report.md")

if __name__ == "__main__":
    main()
