from pathlib import Path

import typer

from fly.services.git import Git


def init(name: str | None = None):
    if not Git.is_repository():
        typer.echo("Not inside a git repository.", err=True)
        raise typer.Exit(code=1)

    if name is None:
        name = Path(Git.get_repository_root()).name

    typer.echo(name)
