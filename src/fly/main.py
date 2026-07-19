import typer

from fly.callbacks.version import get_version
from fly.commands.init import init

app = typer.Typer()


@app.callback(invoke_without_command=True)
def main(
    version: bool = typer.Option(
        False, "--version", "-v", help="Print version information", is_eager=True
    ),
):
    if version:
        get_version()
        raise typer.Exit()


app.command()(init)
