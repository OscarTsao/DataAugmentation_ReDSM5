"""CLI smoke tests."""
import subprocess
import os

def test_cli_help():
    env = os.environ.copy()
    env["PYTHONPATH"] = "/home/oscartsao/Developer/DataAugmentation_ReDSM5"
    result = subprocess.run(
        ["python", "tools/generate_augsets.py", "--help"], 
        capture_output=True,
        env=env,
        cwd="/home/oscartsao/Developer/DataAugmentation_ReDSM5"
    )
    assert result.returncode == 0
    assert b"--input" in result.stdout
    assert b"--combo-mode" in result.stdout

def test_cli_required_args():
    env = os.environ.copy()
    env["PYTHONPATH"] = "/home/oscartsao/Developer/DataAugmentation_ReDSM5"
    result = subprocess.run(
        ["python", "tools/generate_augsets.py"], 
        capture_output=True,
        env=env,
        cwd="/home/oscartsao/Developer/DataAugmentation_ReDSM5"
    )
    assert result.returncode != 0  # Should fail without required args
