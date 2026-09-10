import subprocess

import typer


class GitUtils:
    @staticmethod
    def run_git(*args: str) -> str | None:
        try:
            result = subprocess.run(
                ["git", *args], capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None

    @staticmethod
    def check_git() -> None:
        if not (GitUtils.run_git("rev-parse", "--is-inside-work-tree") == "true"):
            typer.echo("Not inside a Git repository.", err=True)
            raise typer.Exit(code=1)
