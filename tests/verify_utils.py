"""Shared utilities for verification tests."""
import os
import shutil
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Optional
import pandas as pd
import json

FIXTURES_DIR = Path(__file__).parent / "fixtures"

def load_fixture(name: str = "mini_annotations.csv") -> pd.DataFrame:
    """Load test fixture CSV."""
    path = FIXTURES_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Fixture not found: {path}")
    return pd.read_csv(path)

@contextmanager
def temp_output_dir(prefix="verify_"):
    """Create temporary output directory that auto-cleans."""
    tmpdir = tempfile.mkdtemp(prefix=prefix)
    try:
        yield Path(tmpdir)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

def is_cuda_available() -> bool:
    """Check if CUDA is available."""
    try:
        import torch
        return torch.cuda.is_available()
    except ImportError:
        return False

def run_cli(*args, cwd=None) -> tuple[int, str, str]:
    """Run CLI and return (exit_code, stdout, stderr)."""
    import subprocess
    result = subprocess.run(
        ["python", "tools/generate_augsets.py", *args],
        cwd=cwd or Path.cwd(),
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr

def parse_meta_json(path: Path) -> dict:
    """Parse meta.json from combo output."""
    return json.loads((path / "meta.json").read_text())
