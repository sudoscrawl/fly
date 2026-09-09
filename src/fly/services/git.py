import subprocess
from fly.helpers.git import GitUtils


class Git:
    @staticmethod
    def is_repository() -> bool:
        return GitUtils.run_git("rev-parse", "--is-inside-work-tree") == True

    @staticmethod
    def get_repository_root() -> str:
        return GitUtils.run_git("rev-parse", "--show-toplevel")  # type: ignore
