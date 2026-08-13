
import typer

from fly.services.fileio import FileIO
from fly.services.git import Git
from fly.services.helpers import Helpers


def init(name: str | None = None):

    Helpers.check_git()

    project_root = Helpers.get_proj_root_path(Git.get_repository_root())

    if name is None:
        name = project_root.name
    if FileIO.check_if_initialized(project_root):
        typer.echo("Project is already initialized with fly.", err=True)
        raise typer.Exit(code=1)

    FileIO.create_fly_dir(project_root)
    FileIO.initialize_project(project_root, name)
    FileIO.update_gitignore(Git.get_repository_root())

    typer.echo("Your project has been initialized with fly.")
    raise typer.Exit()
