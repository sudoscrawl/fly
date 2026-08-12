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
    if FileIO.check_if_initialized(project_root):
        typer.echo("Project is already initialized with fly.", err=True)
        raise typer.Exit(code=1)

    FileIO.create_fly_dir(project_root)
    FileIO.initialize_notes(project_root)
    FileIO.update_gitignore(Git.get_repository_root())

    typer.echo("Your project has been initialized with fly.")
    raise typer.Exit()
