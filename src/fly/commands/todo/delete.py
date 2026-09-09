import typer

from fly.helpers.git import GitUtils
from fly.helpers.json import JSON
from fly.helpers.utils import Utils


def delete(todo_id: str) -> None:
    """Delete a note

    Args:
        todo_id: The id of the todo to get deleted.
    """

    GitUtils.check_git()

    project_root = Utils.get_project_root_path()

    Utils.is_fly_initialized()

    todo_file = project_root / ".fly/todo.json"

    todos = JSON.load_json(todo_file)

    if not todos:
        typer.echo(
            "This project does not contain any todos.\nUse fly todo add to create some todos for yourself.",
            err=True,
        )
        raise typer.Exit(code=1)

    todo_obj = next(todo for todo in todos if todo["id"] == todo_id)

    if todo_obj is None:
        typer.echo(f"Note with ID: {todo_id} was not found.", err=True)
        raise typer.Exit(code=1)

    todos.remove(todo_obj)
    JSON.render_json(todo_file, todos)

    typer.echo("The todo has been erased.")
    raise typer.Exit(code=0)
