import json
import subprocess
from pathlib import Path


def test_parse_valid_har():
    har_file = Path("tests/fixtures/valid.har")
    output_dir = Path("tests/output_valid")
    
    if output_dir.exists():
        import shutil
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    # Run the CLI command
    import os
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()
    
    result = subprocess.run(
        [".venv/bin/python3", "src/cli/main.py", "parse", "--har", str(har_file), "--output", str(output_dir)],
        capture_output=True,
        text=True,
        env=env
    )


    assert result.returncode == 0
    
    req_file = output_dir / "req_0001.json"
    res_file = output_dir / "res_0001.json"
    
    assert req_file.exists()
    assert res_file.exists()
    
    with open(req_file) as f:
        req_data = json.load(f)
        assert req_data["method"] == "GET"
        assert req_data["url"] == "https://example.com/api/test"
        
    with open(res_file) as f:
        res_data = json.load(f)
        assert res_data["status"] == 200
        assert res_data["content"]["text"] == '{"status": "ok"}'
