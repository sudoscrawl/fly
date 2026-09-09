import json
import os
import uuid

import pendulum
import typer

from fly.services.fileio import FileIO
from fly.services.git import Git
from fly.helpers.git import GitUtils
from fly.helpers.utils import Utils
from fly.helpers.json import JSON


def add(note: list[str]) -> None:
    """Appends a note

    Args:
        note: The message which you want to note / remember

    """
    message = " ".join(note)

    GitUtils.check_git()

    project_root = Utils.get_project_root_path()
    Utils.is_fly_initialized()

    notes_file = project_root / ".fly/notes.json"

    notes = JSON.load_json(notes_file)

    timezone = os.environ.get("TZ", "UTC")
    obj = {
        "id": str(uuid.uuid4())[:7],
        "note": message,
        "timestamp": pendulum.now(timezone).to_iso8601_string(),
    }

    notes.append(obj)

    JSON.render_json(notes_file, notes)

    typer.echo("Noted.")
    raise typer.Exit(code=0)
