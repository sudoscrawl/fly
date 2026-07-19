from pathlib import Path


class FileIO:
    @staticmethod
    def create_fly_dir(path: Path):
        fly_dir = path / ".fly"
        fly_dir.mkdir(exist_ok=True)
