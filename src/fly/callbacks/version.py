import typer
from fly import __version__

def get_version():
    typer.echo(f"fly version {__version__}")
