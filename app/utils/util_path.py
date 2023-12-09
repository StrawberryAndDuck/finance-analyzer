from pathlib import Path


def get_repository_path():
    current_abs_path = Path(".").absolute().__str__()
    dirs = current_abs_path.split("/")
    repo_path_idx = dirs.index("SlackChannels")
    repo_path = "/".join(dirs[: repo_path_idx + 1])
    return Path(repo_path)
