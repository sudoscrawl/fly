from pathlib import Path

import typer

from fly.services.fileio import FileIO
from fly.services.git import Git


class Utils:
    @staticmethod
    def get_project_root_path() -> Path:
        return Path(Git.get_repository_root())

    @staticmethod
    def is_fly_initialized() -> None:
        if not FileIO.check_if_initialized(Path(Git.get_repository_root())):
            typer.echo(
                "This project has not been initialized with fly.\nRun fly init to initialize.",
                err=True,
            )
            raise typer.Exit(code=1)
