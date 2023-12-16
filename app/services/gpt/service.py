import json
from openai import OpenAI

from app.utils.util_path import get_repository_path


def init_openai_client():
    repo_path = get_repository_path()
    with open(repo_path.joinpath("app/services/slack/secrets/secret.json"), "r") as f:
        secret = json.load(f)
        return OpenAI(api_key=secret.get("bot-token"))


def query_with_prompt(client: OpenAI, model: str, prompt: str):
    return client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )
