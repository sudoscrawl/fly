from typing import Annotated

import typer
from rich.console import Console

from fly.callbacks.version import get_version
from fly.commands.init import init
from fly.commands.note.add import add as add_note
from fly.commands.note.delete import delete as delete_note
from fly.commands.note.view import view as view_note
from fly.commands.todo.add import add as add_todo
from fly.commands.todo.complete import complete as complete_todo
from fly.commands.todo.delete import delete as delete_todo
from fly.commands.todo.incomplete import incomplete as incomplete_todo
from fly.commands.todo.view import view as view_todo
from fly.commands.where_was_i import where_was_i

app = typer.Typer()
note = typer.Typer(help="Create and manage notes for your project.")
todo = typer.Typer(help="Create and manage todos for your project.")

app.add_typer(note, name="note")
app.add_typer(todo, name="todo")

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
app.command("where-was-i", help="Get information on your progress")(where_was_i)

note.command(help="Create a note")(add_note)
note.command(help="Take a look at your existing notes")(view_note)
note.command(help="Delete one of the existing notes")(delete_note)

todo.command(help="Add a todo")(add_todo)
todo.command(help="Delete one of the existing todos")(delete_todo)
todo.command(help="Take a look at your existing todos")(view_todo)
todo.command(help="Change the status of a todo as completed")(complete_todo)
todo.command(help="Change the status of a todo as incomplete")(incomplete_todo)
