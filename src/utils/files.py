import json
from pathlib import Path
from typing import Any


def write_json_file(file_path: Path, data: Any) -> None:
    """Writes data to a JSON file with indentation."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
