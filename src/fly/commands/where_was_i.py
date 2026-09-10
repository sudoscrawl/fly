import typer
from fly.helpers.utils import Utils
from fly.helpers.git import GitUtils
from fly.helpers.json import JSON


def where_was_i() -> None:
    
    GitUtils.check_git()

    project_root = Utils.get_project_root_path()

    Utils.is_fly_initialized()

    todo_file = project_root / ".fly/todo.json"
    notes_file = project_root / ".fly/notes.json"

    notes = JSON.load_json(notes_file)
    todos = JSON.load_json(todo_file)

    typer.secho(
        f"{project_root.name}",
        bold = True        
    )
    typer.echo(str(project_root))
