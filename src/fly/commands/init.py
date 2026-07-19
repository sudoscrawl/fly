from pathlib import Path

import typer

from fly.services.fileio import FileIO
from fly.services.git import Git


def init(name: str | None = None):
    if not Git.is_repository():
        typer.echo("Not inside a git repository.", err=True)
        raise typer.Exit(code=1)

    project_root = Path(Git.get_repository_root())

    if name is None:
        name = project_root.name

    FileIO.create_fly_dir(project_root)
