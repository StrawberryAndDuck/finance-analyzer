import json
from app.utils.util_path import get_repository_path

from openai import OpenAI


def init_openai_client():
    repo_path = get_repository_path()
    with open(repo_path.joinpath("app/services/slack/secrets/secret.json"), "r") as f:
        secret = json.load(f)
        return OpenAI(api_key=secret.get("bot-token"))
