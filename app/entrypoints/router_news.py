from fastapi import APIRouter

from app.dtos.dto_news import RequestAgricultureNewsDTO, ResponseAgricultureNewsDTO
from app.services.gpt.service import query_with_prompt
from app.services.slack.channels.agriculture_news.service import alert_message

router = APIRouter(prefix="/news")


@router.post("/agriculture", response_model=ResponseAgricultureNewsDTO)
def request_agriculture_news(params: RequestAgricultureNewsDTO):
    response = query_with_prompt(model="gpt-4", prompt="오늘자로 농수산물에 대한 최신뉴스들을 정리해서 알려줘.")
    message = response["choices"][0]["message"]["content"]
    alert_message(message=message)
    return response
