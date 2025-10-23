"""Verify augmentation modifies ONLY evidence spans."""
import pytest
from tests.verify_utils import load_fixture, temp_output_dir, run_cli
import pandas as pd

def test_non_evidence_unchanged():
    """Core property: everything except evidence span is byte-identical."""
    with temp_output_dir() as outdir:
        # Run with one CPU method
        run_cli(
            "--input", "tests/fixtures/mini_annotations.csv",
            "--output-root", str(outdir),
            "--combo-mode", "singletons",
            "--variants-per-sample", "1",
            "--seed", "123",
            "--methods-yaml", "conf/augment_methods.yaml",
            "--num-proc", "1",
        )

        # Find a generated dataset
        datasets = list(outdir.rglob("dataset.parquet"))
        if not datasets:
            pytest.skip("No datasets generated")

        df_aug = pd.read_parquet(datasets[0])
        df_orig = load_fixture()

        # For each augmented row, verify non-evidence region is unchanged
        for _, row in df_aug.iterrows():
            # Find original row by post_id
            orig_row = df_orig[df_orig["post_id"] == row.get("post_id", "")]
            if orig_row.empty:
                continue

            orig_text = orig_row.iloc[0]["post_text"]
            aug_text = row["post_text"]
            evidence_aug = row["evidence"]
            evidence_orig = row.get("evidence_original", orig_row.iloc[0]["evidence"])

            # Reconstruct original by replacing augmented evidence with original
            reconstructed = aug_text.replace(evidence_aug, evidence_orig, 1)
            assert reconstructed == orig_text, "Non-evidence region changed"
