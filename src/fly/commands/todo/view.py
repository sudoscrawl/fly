import json
from typing import Annotated

import pendulum
import typer

from fly.services.fileio import FileIO
from fly.services.git import Git
from fly.services.helpers import Helpers


def view(
    todo_id: Annotated[
        str | None, typer.Option("--id", help="View a specific todo using it's id")
    ],
) -> None:
    """Checkout your existing project todos

    Args:
        todo_id: View a specific todo using it's id
    """

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
            "This project does not contain any todos.\nUse fly todo add to create some todos for yourself",
            err=True,
        )
        raise typer.Exit(code=1)

    if todo_id:
        todo_obj = next(todo for todo in todos if todo["id"] == todo_id)

        if todo_obj is None:
            typer.echo(f"The todo with ID: {todo_id} was not found.", err=True)
            raise typer.Exit(code=1)

        dt = pendulum.parse(todo_obj["timestamp"])
        typer.echo(
            f"ID: {todo_obj['id']}\nTASK: {todo_obj['task']}\nCOMPLETED: {bool(todo_obj['completed'])}\nTIMESTAMP: {dt}"
        )
        raise typer.Exit(code=0)

    for todo in todos:
        dt = pendulum.parse(todo["timestamp"])
        typer.echo(
            f"ID: {todo['id']}\nTASK: {todo['task']}\nCOMPLETED: {bool(todo['completed'])}\nTIMESTAMP: {dt}"
        )
    raise typer.Exit(code=0)
