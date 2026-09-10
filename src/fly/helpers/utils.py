import pendulum
import os
from pathlib import Path

import typer

from fly.services.fileio import FileIO
from fly.services.git import Git


class Utils:
    @staticmethod
    def get_project_root_path() -> Path:
        return Path(Git.get_repository_root())

    @staticmethod
    def is_fly_initialized() -> None:
        if not FileIO.check_if_initialized(Path(Git.get_repository_root())):
            typer.echo(
                "This project has not been initialized with fly.\nRun fly init to initialize.",
                err=True,
            )
            raise typer.Exit(code=1)

    @staticmethod
    def get_timezone() -> str:
        return os.environ.get("TZ", "UTC")

    @staticmethod
    def get_timestamp() -> str:
        timezone = Utils.get_timezone()
        return pendulum.now(timezone).to_iso8601_string()

    @staticmethod
    def get_relative_time(timestamp: str) -> str:
        now = pendulum.now(Utils.get_timezone())
        period = now - pendulum.parse(timestamp)  # type: ignore
        difference = max(0, period.total_seconds())

        if difference < 60:
            return "just now"

        minutes = difference // 60

        if minutes < 60:
            return f"{minutes}m ago"

        hours = minutes // 60

        if hours < 24:
            return f"{hours}h ago"

        days = hours // 24

        if days < 7:
            return f"{days}d ago"

        weeks = days // 7

        if weeks < 5:
            return f"{weeks}w ago"

        return f"{days // 30}mo ago"
