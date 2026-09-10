import typer


class TyperUtils:
    @staticmethod
    def display_section(text: str) -> None:
        typer.echo()
        typer.secho(text, bold=True)
