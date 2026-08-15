import json
import os
import uuid

import pendulum
import typer

from fly.services.fileio import FileIO
from fly.services.git import Git
from fly.services.helpers import Helpers


def remember(note: list[str]) -> None:

    message = " ".join(note)

    Helpers.check_git()

    project_root = Helpers.get_proj_root_path(Git.get_repository_root())

    if not FileIO.check_if_initialized(project_root):
        typer.echo(
            "This project has not been initialized with fly.\n Run fly init to initialize."
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

    timezone = os.environ.get("TZ", "UTC")
    obj = {
        "id": str(uuid.uuid4()),
        "note": message,
        "timestamp": pendulum.now(timezone).to_iso8601_string(),
    }

    notes.append(obj)

    notes_file.write_text(json.dumps(notes, indent=2) + "\n")

    typer.echo("Noted.")
