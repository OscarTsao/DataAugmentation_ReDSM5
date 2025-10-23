#!/usr/bin/env python3
"""Generate verification reports."""
import json
from pathlib import Path
from datetime import datetime

def main():
    # Load test results
    test_results_path = Path("test_results.json")
    if test_results_path.exists():
        with open(test_results_path) as f:
            test_data = json.load(f)
        total = test_data["summary"]["total"]
        passed = test_data["summary"].get("passed", 0)
        failed = test_data["summary"].get("failed", 0)
        xfailed = test_data["summary"].get("xfailed", 0)
    else:
        total = passed = failed = xfailed = 0

    # Load benchmark results
    bench_path = Path("benchmark_results.json")
    if bench_path.exists():
        with open(bench_path) as f:
            bench_data = json.load(f)
    else:
        bench_data = []

    # Generate summary JSON
    summary = {
        "timestamp": datetime.now().isoformat(),
        "test_summary": {
            "total": total,
            "passed": passed,
            "failed": failed,
            "xfailed": xfailed,
        },
        "benchmark_summary": bench_data,
        "status": "pass" if failed == 0 else "fail",
    }

    with open("verification_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    # Generate markdown report
    report = f"""# Verification Report

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Test Results

| Metric | Count |
|--------|-------|
| Total  | {total} |
| Passed | {passed} |
| Failed | {failed} |
| XFailed | {xfailed} |

**Status:** {'✅ PASS' if failed == 0 else '❌ FAIL'}

## Benchmarks

| Subset | Rows | Duration (s) | Throughput (rows/s) |
|--------|------|--------------|---------------------|
"""

    for bench in bench_data:
        report += f"| {bench['subset']} | {bench['rows']} | {bench['duration_sec']} | {bench['rows_per_sec']} |\n"

    report += "\n## Recommendations\n\n"
    if failed > 0:
        report += "- ❌ Some tests failed. Review test_results.json for details.\n"
    else:
        report += "- ✅ All tests passed. Verification complete.\n"

    with open("verification_report.md", "w") as f:
        f.write(report)

    print("✓ Reports generated: verification_summary.json, verification_report.md")

if __name__ == "__main__":
    main()
