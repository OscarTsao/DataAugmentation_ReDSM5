#!/bin/bash
# Comprehensive verification orchestration
set -e

echo "=== [SETUP] Installing dependencies ==="
bash tools/verify/setup_env.sh

echo ""
echo "=== [TESTS] Running pytest verification suite ==="
pytest tests/verify/ -v --json-report --json-report-file=test_results.json || true

echo ""
echo "=== [BENCH] Running micro-benchmarks ==="
python3 tools/verify/bench_small.py || true

echo ""
echo "=== [REPORT] Generating reports ==="
python3 tools/verify/generate_report.py

echo ""
echo "=== [DONE] Verification complete ==="
echo "See verification_report.md for results"
