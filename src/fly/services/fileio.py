from pathlib import Path


class FileIO:
    @staticmethod
    def create_fly_dir(path: Path):
        fly_dir = path / ".fly"
        fly_dir.mkdir(exist_ok=True)

    @staticmethod
    def update_gitignore(path: str):
        gitignore_path = f"{path}/.gitignore"
        strings = ["\n", "# Fly\n", ".fly\n"]

        with open(gitignore_path, "a") as file:
            file.writelines(strings)
