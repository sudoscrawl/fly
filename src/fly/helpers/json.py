import json
from pathlib import Path


class JSON:
    @staticmethod
    def load_json(path: Path) -> list:
        if not path.exists():
            return []

        try:
            return json.loads(path.read_text())
        except json.JSONDecodeError:
            return []

    @staticmethod
    def render_json(path: Path, text: str) -> None:
        if not path.exists():
            raise FileNotFoundError

        path.write_text(json.dumps(text, indent=2) + "\n")
