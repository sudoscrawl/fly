import typer

from fly.helpers.git import GitUtils
from fly.helpers.json import JSON
from fly.helpers.utils import Utils


def incomplete(todo_id: str) -> None:
    """Marks a todo back as incomplete

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
            "This project does not contain any todos.\nUse fly todo add to create some todos for yourself",
            err=True,
        )
        raise typer.Exit(code=1)

    todo_obj = next(todo for todo in todos if todo["id"] == todo_id)

    if todo_obj is None:
        typer.echo(f"Todo with ID: {todo_id} was not found", err=True)
        raise typer.Exit(code=1)

    if not todo_obj["completed"]:
        typer.echo("Your todo was already marked as incomplete")
        raise typer.Exit(code=0)
    todo_obj["completed"] = 0

    JSON.render_json(todo_file, todos)

    typer.echo("Your todo has been marked as incomplete")
    raise typer.Exit(code=0)
