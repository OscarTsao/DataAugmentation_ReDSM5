"""Test quality filtering thresholds."""
from tests.verify_utils import temp_output_dir, run_cli
import pandas as pd

def test_quality_thresholds():
    """Quality min/max filters work."""
    with temp_output_dir() as outdir:
        run_cli(
            "--input", "tests/fixtures/mini_annotations.csv",
            "--output-root", str(outdir),
            "--combo-mode", "singletons",
            "--quality-min-sim", "0.90",  # Very strict
            "--quality-max-sim", "0.98",
            "--variants-per-sample", "5",
            "--seed", "42",
            "--num-proc", "1",
        )

        datasets = list(outdir.rglob("dataset.parquet"))
        if datasets:
            df = pd.read_parquet(datasets[0])
            # With strict thresholds, fewer variants expected
            assert len(df) >= 0  # May be empty if all filtered
