import json

from slack_sdk import WebClient

from app.utils.util_path import get_repository_path


def init_slack_bot():
    repo_path = get_repository_path()
    with open(repo_path.joinpath("app/services/slack/secrets/secret.json"), "r") as f:
        secret = json.load(f)
        return WebClient(token=secret.get("bot-token"))


bot = init_slack_bot()


def alert_message(message: str):
    bot.chat_meMessage(channel="test-channel", text=message)
