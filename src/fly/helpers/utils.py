from pathlib import Path
from fly.services.fileio import FileIO
import typer


class Utils:
    @staticmethod
    def get_project_root_path(path: str) -> Path:
        return Path(path)

    @staticmethod
    def is_fly_initialized(path: Path) -> None:
        if not FileIO.check_if_initialized(path):
            typer.echo(
                "This project has not been initialized with fly.\nRun fly init to initialize.",
                err=True,
            )
            raise typer.Exit(code=1)
