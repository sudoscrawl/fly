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


def add(task: list[str]) -> None:
    """Creates a new todo

    Args:
        task: the task to get stored
    """

    todo = " ".join(task)

    GitUtils.check_git()

    project_root = Utils.get_project_root_path()

    Utils.is_fly_initialized()

    todo_file = project_root / ".fly/todo.json"
    todos = JSON.load_json(todo_file)

    timezone = os.environ.get("TZ", "UTC")

    obj = {
        "id": str(uuid.uuid4())[:7],
        "task": todo,
        "completed": 0,
        "timestamp": pendulum.now(timezone).to_iso8601_string(),
    }

    todos.append(obj)

    JSON.render_json(todo_file, todos)

    typer.echo("Task has been added.")
    raise typer.Exit(code=0)
