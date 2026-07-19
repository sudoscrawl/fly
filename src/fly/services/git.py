import subprocess


class Git:
    @staticmethod
    def is_repository() -> bool:
        res = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            text=True,
        )
        return res.stdout.strip() == "true"

    @staticmethod
    def get_repository_root() -> str:
        res = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
        )
        return res.stdout.strip()
