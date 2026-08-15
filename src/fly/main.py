from typing import Annotated

import typer
from rich.console import Console

from fly.callbacks.version import get_version
from fly.commands.init import init
from fly.commands.note.add import add
from fly.commands.note.view import view

app = typer.Typer()
note = typer.Typer(help="Create and manage notes for your project.")

app.add_typer(note, name="note")

console = Console()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Annotated[
        bool,
        typer.Option(
            "--version", "-v", help="Print version information", is_eager=True
        ),
    ] = False,
):

    if version:
        get_version()
        raise typer.Exit()

    if ctx.invoked_subcommand is None:
        console.print("[bold cyan]fly[/bold cyan]")
        console.print("[italic dim]Your project's second memory.[/italic dim]\n")

        console.print("Use fly --help to get a list of all available commands")
        raise typer.Exit()


app.command(help="Initialize a project")(init)
note.command(help="Create a note")(add)
note.command(help="Take a look at your existing notes")(view)
