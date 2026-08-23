import json

import typer

from fly.services.fileio import FileIO
from fly.services.git import Git
from fly.services.helpers import Helpers


def complete(todo_id: str) -> None:
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

    if not todos:
        typer.echo(
            "This project does not contain any existing todos.\nUse fly todo add to create some todos for yourself.",
            err=True,
        )
        raise typer.Exit(code=1)

    todo_obj = next(todo for todo in todos if todo["id"] == todo_id)

    if todo_obj is None:
        typer.echo(f"Todo with ID: {todo_id} was not found", err=True)
        raise typer.Exit(code=1)

    if todo_obj["completed"]:
        typer.echo("Your todo was already marked as completed.")
        raise typer.Exit(code=0)
    else:
        todo_obj["completed"] = 1

    todo_file.write_text(json.dumps(todos, indent=2) + "\n")

    typer.echo("Todo has been marked as completed.")
    raise typer.Exit(code=0)
