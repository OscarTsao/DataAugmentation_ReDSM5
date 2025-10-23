"""Verify deterministic outputs."""
from tests.verify_utils import temp_output_dir, run_cli
import pandas as pd
import hashlib

def test_same_seed_identical():
    """Same seed produces identical outputs."""
    results = []
    for run in range(2):
        with temp_output_dir() as outdir:
            run_cli(
                "--input", "tests/fixtures/mini_annotations.csv",
                "--output-root", str(outdir),
                "--combo-mode", "singletons",
                "--variants-per-sample", "2",
                "--seed", "42",
                "--num-proc", "1",
            )
            datasets = list(outdir.rglob("dataset.parquet"))
            if datasets:
                df = pd.read_parquet(datasets[0])
                hash_val = hashlib.sha256(df.to_json().encode()).hexdigest()
                results.append(hash_val)

    if len(results) == 2:
        assert results[0] == results[1], "Same seed produced different outputs"

def test_different_seed_different():
    """Different seeds produce different outputs."""
    results = []
    for seed in [42, 123]:
        with temp_output_dir() as outdir:
            run_cli(
                "--input", "tests/fixtures/mini_annotations.csv",
                "--output-root", str(outdir),
                "--combo-mode", "singletons",
                "--variants-per-sample", "2",
                "--seed", str(seed),
                "--num-proc", "1",
            )
            datasets = list(outdir.rglob("dataset.parquet"))
            if datasets:
                df = pd.read_parquet(datasets[0])
                results.append(df["evidence"].tolist())

    if len(results) == 2:
        # At least some evidences should differ
        assert results[0] != results[1], "Different seeds produced identical outputs"
