from typing import Annotated

import pendulum
import typer

from fly.helpers.git import GitUtils
from fly.helpers.json import JSON
from fly.helpers.utils import Utils


def view(
    note_id: Annotated[
        str | None, typer.Option("--id", help="View a specific note using it's id")
    ] = None,
) -> None:
    """Checkout your existing project notes

    Args:
        id: provide the specific of the note and only access that
    """

    GitUtils.check_git()

    project_root = Utils.get_project_root_path()

    Utils.is_fly_initialized()

    notes_file = project_root / ".fly/notes.json"

    notes = JSON.load_json(notes_file)

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
            f"ID: {note['id']}\nNOTE: {note['note']}\nTIMESTAMP: {dt.format('MMMM D YYYY h:mm A')}"  # pyright: ignore
        )
        typer.echo("------")
    raise typer.Exit(code=0)
