import contextvars
import json
import logging
import logging.handlers
import os
import socket
from datetime import datetime
from logging import LogRecord
from typing import Any, Union

import pytz
import requests

fmt = f"%(asctime)s | %(levelname)s | {socket.gethostname()} | %(module)s:%(lineno)d | %(message)s"


class KSTFormatter(logging.Formatter):
    def __init__(
        self,
        fmt: Union[str, None] = None,
        datefmt: Union[str, None] = None,
        style="%",
        validate: bool = True,
        cutoff: bool = False,
        max_message_length: int = 1000,
    ) -> None:
        super().__init__(fmt, datefmt, style, validate)
        self.cutoff = cutoff
        self.max_message_length = max_message_length

    def format(self, record: LogRecord):
        original_message = super().format(record)
        original_message = original_message.encode("utf-8").decode("utf-8")
        return original_message

    def converter(self, timestamp: Any):
        return datetime.fromtimestamp(timestamp, pytz.timezone("Asia/Seoul"))

    def formatTime(self, record: LogRecord, datefmt: str = None):
        dt = self.converter(record.created)
        if datefmt is not None:
            return dt.strftime(datefmt)
        return dt.isoformat()


class SlackLoggingHandler(logging.Handler):
    def __init__(
        self,
        token: str,
        channel: str,
    ):
        super().__init__()
        self.post_api_url = "https://slack.com/api/chat.postMessage"
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {self.token}",
        }
        self.channel = channel
        self.sep = "|"

    def emit(self, record: LogRecord):
        log = self.format(record)
        elems = log.split(self.sep)
        response = requests.post(
            url=self.post_api_url,
            headers=self.headers,
            json={
                "channel": self.channel,
                "blocks": [
                    {
                        "type": "section",
                        "fields": [
                            {"type": "mrkdwn", "text": f"*Timestamp:*\n{elems[0]}"},
                            {"type": "mrkdwn", "text": f"*Title:*\n{elems[4]}"},
                        ],
                    },
                ],
            },
        )
        response = requests.post(
            url=self.post_api_url,
            headers=self.headers,
            json={
                "channel": self.channel,
                "thread_ts": json.loads(response.text)["ts"],
                "text": f"```Title: {elems[4]}\n{self.sep.join(elems[5:])}```",
            },
        )


class CustomLogger(logging.Logger):
    def __init__(self, name: str) -> None:
        super().__init__(name=name)
        self.init_custom_logger_obj()

    def init_custom_logger_obj(self):
        formatter_cutoff = KSTFormatter(fmt=fmt, cutoff=True)
        slack_log_handler = SlackLoggingHandler(
            token=os.getenv("SLACK_TOKEN"),
            channel=os.getenv("SLACK_CHANNEL"),
        )
        slack_log_handler.setFormatter(formatter_cutoff)
        self.addHandler(slack_log_handler)

        self.propagate = True


logger = CustomLogger("finance")
