import json
import os
import subprocess
from pathlib import Path


def test_decode_base64_har():
    har_file = Path("tests/fixtures/base64.har")
    output_dir = Path("tests/output_base64")
    
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

    assert result.returncode == 0
    
    res_file = output_dir / "res_0001.json"
    assert res_file.exists()
    
    with open(res_file) as f:
        res_data = json.load(f)
        # It should be decoded: eyJzdGF0dXMiOiAib2sifQ== -> {"status": "ok"}
        assert res_data["content"]["text"] == '{"status": "ok"}'
        # The 'encoding' field should be removed (T016)
        assert "encoding" not in res_data["content"]
