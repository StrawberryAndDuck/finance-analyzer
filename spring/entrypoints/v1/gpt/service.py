import os

from openai import OpenAI
from openai.types.chat import ChatCompletion
from redis import Redis

redis_client = Redis(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    db=os.getenv("REDIS_DB"),
    password=os.getenv("REDIS_PASSWORD"),
)


def init_openai_client():
    credential = redis_client.get("openai-credential")
    api_key = credential.get("client-token")
    return OpenAI(api_key=api_key)


openai_client = init_openai_client()


def query_with_prompt(model: str, prompt: str) -> ChatCompletion:
    return openai_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    ).model_dump()
