import typer

from fly.helpers.git import GitUtils
from fly.helpers.json import JSON
from fly.helpers.utils import Utils


def complete(todo_id: str) -> None:
    """Marks a todo as completed

    Args:
        todo_id: ID of the todo
    """

    GitUtils.check_git()

    project_root = Utils.get_project_root_path()

    Utils.is_fly_initialized()

    todo_file = project_root / ".fly/todo.json"

    todos = JSON.load_json(todo_file)

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
    todo_obj["completed"] = 1

    JSON.render_json(todo_file, todos)

    typer.echo("Todo has been marked as completed.")
    raise typer.Exit(code=0)
