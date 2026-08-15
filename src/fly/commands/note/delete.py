import json

import typer

from fly.services.fileio import FileIO
from fly.services.git import Git
from fly.services.helpers import Helpers


def delete(note_id: str) -> None:
    """Delete a note

    Args:
        id: The id of the note you want to delete
    """
    Helpers.check_git()

    project_root = Helpers.get_proj_root_path(Git.get_repository_root())

    if not FileIO.check_if_initialized(project_root):
        typer.echo(
            "This project has not been initialized with fly.\nRun fly init to initialize.",
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

    note_obj = next(note for note in notes if note["id"] == note_id)

    if note_obj is None:
        typer.echo(f"Note with ID {note_id}", err=True)
        raise typer.Exit(code=1)
    notes.remove(note_obj)
    notes_file.write_text(json.dumps(notes, indent=2) + "\n")

    typer.echo("The note has been erased.")
    raise typer.Exit(code=0)
