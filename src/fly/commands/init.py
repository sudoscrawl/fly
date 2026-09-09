import typer

from fly.services.fileio import FileIO
from fly.helpers.git import GitUtils
from fly.helpers.utils import Utils


def init(name: str | None = None):

    GitUtils.check_git()

    project_root = Utils.get_project_root_path()

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
