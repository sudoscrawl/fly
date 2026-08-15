import json
from typing import Annotated

import pendulum
import typer

from fly.services.fileio import FileIO
from fly.services.git import Git
from fly.services.helpers import Helpers


def view(
    note_id: Annotated[
        str | None, typer.Option("--id", help="View a specific note using it's id")
    ] = None,
) -> None:
    """Checkout your existing project notes

    Args:
        id: provide the specific of the note and only access that
    """

    Helpers.check_git()

    project_root = Helpers.get_proj_root_path(Git.get_repository_root())

    if not FileIO.check_if_initialized(project_root):
        typer.echo(
            "This project has not been initialized with fly.\nRun fly to initialize.",
            err=True,
        )
        raise typer.Exit(code=1)

    notes_file = project_root / ".fly/notes.json"

    if notes_file.exists():
        try:
            notes = json.loads(notes_file.read_text())
        except json.JSONDecodeError:
            notes = []
    else:
        notes = []

    if not notes:
        typer.echo(
            "This project does not contain any notes.\nUse fly note add to create some notes for yourself.",
            err=True,
        )
        raise typer.Exit(code=1)

    if note_id:
        note_obj = next((note for note in notes if note["id"] == note_id), None)

        if note_obj is None:
            typer.echo(f"Note with ID {note_id} was not found.", err=True)
            raise typer.Exit(code=1)

        dt = pendulum.parse(note_obj["timestamp"])
        typer.echo(
            f"ID: {note_id}\nNOTE: {note_obj['note']}\nTIMESTAMP: {dt.format('MMMM D YYYY h:mm A')}"  # pyright: ignore
        )
        raise typer.Exit(code=0)
    for note in notes:
        dt = pendulum.parse(note["timestamp"])
        typer.echo(
            f"ID: {note_id}\nNOTE: {note['note']}\nTIMESTAMP: {dt.format('MMMM D YYYY h:mm A')}"  # pyright: ignore
        )
        typer.echo("------")
        raise typer.Exit(code=0)
