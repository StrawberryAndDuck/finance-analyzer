import json
from openai import OpenAI
from openai.types.chat import ChatCompletion

from app.utils.util_path import get_repository_path


def init_openai_client():
    repo_path = get_repository_path()
    with open(repo_path.joinpath("app/services/gpt/secrets/secret.json"), "r") as f:
        secret = json.load(f)
        return OpenAI(api_key=secret.get("client-token"))


client = init_openai_client()


def query_with_prompt(model: str, prompt: str) -> ChatCompletion:
    return client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    ).model_dump()
