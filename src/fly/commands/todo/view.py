from typing import Annotated

import pendulum
import typer

from fly.helpers.git import GitUtils
from fly.helpers.json import JSON
from fly.helpers.utils import Utils


def view(
    todo_id: Annotated[
        str | None, typer.Option("--id", help="View a specific todo using it's id")
    ] = None,
) -> None:
    """Checkout your existing project todos

    Args:
        todo_id: View a specific todo using it's id
    """

    GitUtils.check_git()

    project_root = Utils.get_project_root_path()

    Utils.is_fly_initialized()

    todo_file = project_root / ".fly/todo.json"

    todos = JSON.load_json(todo_file)

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
