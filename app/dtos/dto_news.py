from pydantic import BaseModel
from typing import List, Optional


class RequestAgricultureNewsDTO(BaseModel):
    ...


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class Message(BaseModel):
    role: str
    content: str


class Choice(BaseModel):
    message: Message
    finish_reason: str
    index: int
    logprobs: Optional[bool] = None


class ResponseAgricultureNewsDTO(BaseModel):
    id: str
    object: str
    created: int
    model: str
    usage: Usage
    choices: List[Choice]
