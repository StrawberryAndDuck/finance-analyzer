from typing import List, Optional

from pydantic import BaseModel


class RequestGPTDTO(BaseModel):
    prompt: str


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


class ResponseGPTDTO(BaseModel):
    id: str
    object: str
    created: int
    model: str
    usage: Usage
    choices: List[Choice]
