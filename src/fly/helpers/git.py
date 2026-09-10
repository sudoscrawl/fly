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
        if GitUtils.run_git("rev-parse", "--is-inside-work-tree") != "true":
            typer.echo("Not inside a Git repository.", err=True)
            raise typer.Exit(code=1)

    @staticmethod
    def get_git_info() -> dict:
        branch = GitUtils.run_git("branch", "--show-current")
        commit_hash = GitUtils.run_git("rev-parse", "--short", "HEAD")
        commit_message = GitUtils.run_git("log", "-1", "--pretty=%s")
        commit_timestamp = GitUtils.run_git("log", "-1", "--pretty=%ct")
        commit_file = GitUtils.run_git(
            "diff_tree", "--no-commit-id", "--name-only", "-r", "HEAD"
        )
        modified_files = GitUtils.run_git("status", "--short")

        return {
            "branch": branch or "unknown",
            "commit_hash": commit_hash or "unknown",
            "commit_message": commit_message or "No commits",
            "commit_timestamp": commit_timestamp or "unknown",
            "commit_file": (commit_file.splitlines() if commit_file else None),
            "modified_files": (modified_files.splitlines() if modified_files else []),
        }
