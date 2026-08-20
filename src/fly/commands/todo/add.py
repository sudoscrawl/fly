import json
import os
import uuid

import pendulum
import typer

from fly.services.fileio import FileIO
from fly.services.git import Git
from fly.services.helpers import Helpers


def add(task: list[str]) -> None:
    """Creates a new todo

    Args:
        task: the task to get stored
    """

    todo = " ".join(task)

    Helpers.check_git()

    project_root = Helpers.get_proj_root_path(Git.get_repository_root())

    if not FileIO.check_if_initialized(project_root):
        typer.echo(
            "This project has not been initialized with fly.\nRun fly init to initialize.",
            err=True,
        )
        raise typer.Exit(code=1)

    todo_file = project_root / ".fly/todo.json"

    if todo_file.exists():
        try:
            todos = json.loads(todo_file.read_text())
        except json.JSONDecodeError:
            todos = []
    else:
        todos = []

    timezone = os.environ.get("TZ", "UTC")

    obj = {
        "id": str(uuid.uuid4())[:7],
        "task": todo,
        "completed": 0,
        "timestamp": pendulum.now(timezone).to_iso8601_string(),
    }

    todos.append(obj)

    todo_file.write_text(json.dumps(todos, indent=2) + "\n")

    typer.echo("Task has been added.")
    raise typer.Exit(code=0)
