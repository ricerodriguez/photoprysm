import json
from pathlib import Path
from typing import Any

def get_mock_response(name: str) -> dict[str, Any]:
    here = Path(__file__).resolve()
    mock = here.with_name(name).with_suffix('.json').read_text()
    return json.loads(mock)
