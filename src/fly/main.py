import typer
from rich.console import Console

from fly.callbacks.version import get_version
from fly.commands.init import init

app = typer.Typer()

console = Console()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        False, "--version", "-v", help="Print version information", is_eager=True
    ),
):

    if version:
        get_version()
        raise typer.Exit()

    if ctx.invoked_subcommand is None:
        console.print("[bold cyan]Fly[/bold cyan]")
        console.print("[italic dim]Your project's second memory.[/italic dim]\n")

        console.print("Use fly --help to get a list of all available commands")
        raise typer.Exit()


app.command(help="Initialize a project")(init)
