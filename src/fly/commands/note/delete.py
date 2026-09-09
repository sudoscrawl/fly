import typer

from fly.helpers.git import GitUtils
from fly.helpers.json import JSON
from fly.helpers.utils import Utils


def delete(note_id: str) -> None:
    """Delete a note

    Args:
        id: The id of the note you want to delete
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

    note_obj = next(note for note in notes if note["id"] == note_id)

    if note_obj is None:
        typer.echo(f"Note with ID {note_id} was not found", err=True)
        raise typer.Exit(code=1)
    notes.remove(note_obj)

    JSON.render_json(notes_file, notes)

    typer.echo("The note has been erased.")
    raise typer.Exit(code=0)
