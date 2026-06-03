import os
import subprocess
from pathlib import Path


def test_missing_file():
    har_file = Path("tests/fixtures/non_existent.har")
    output_dir = Path("tests/output_errors")
    
    if output_dir.exists():
        import shutil
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()
    
    result = subprocess.run(
        [".venv/bin/python3", "src/cli/main.py", "parse", "--har", str(har_file), "--output", str(output_dir)],
        capture_output=True,
        text=True,
        env=env
    )

    assert result.returncode != 0
    assert "Error" in result.stderr

def test_malformed_json():
    har_file = Path("tests/fixtures/invalid_json.har")
    output_dir = Path("tests/output_errors")
    
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()
    
    result = subprocess.run(
        [".venv/bin/python3", "src/cli/main.py", "parse", "--har", str(har_file), "--output", str(output_dir)],
        capture_output=True,
        text=True,
        env=env
    )

    assert result.returncode != 0
    assert "Error" in result.stderr
