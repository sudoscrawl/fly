from pathlib import Path

import typer

from fly.services.git import Git


class Helpers:
    @staticmethod
    def check_git() -> None:
        if not Git.is_repository():
            typer.echo("Not inside a git repository.", err=True)
            raise typer.Exit(code=1)

    @staticmethod
    def get_proj_root_path(path: str) -> Path:
        return Path(path)
