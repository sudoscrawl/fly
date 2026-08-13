import json
from pathlib import Path


class FileIO:
    @staticmethod
    def check_if_initialized(path: Path) -> bool:
        fly_dir = path / ".fly"

        return fly_dir.is_dir()

    @staticmethod
    def create_fly_dir(path: Path) -> None:
        fly_dir = path / ".fly"
        fly_dir.mkdir(exist_ok=True)

    @staticmethod
    def update_gitignore(path: str) -> None:
        gitignore_path = f"{path}/.gitignore"
        strings = ["\n", "# Fly\n", ".fly\n"]

        with open(gitignore_path, "a") as file:
            file.writelines(strings)

    @staticmethod
    def initialize_project(path: Path, name: str) -> None:
        fly_dir = path / ".fly"

        (fly_dir / "project.json").write_text(
            json.dumps({"name": name}, indent=2) + "\n"
        )
        (fly_dir / "todo.json").write_text("[]\n")
        (fly_dir / "notes.json").write_text("[]\n")
