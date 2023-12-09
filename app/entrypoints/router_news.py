from fastapi import APIRouter

from app.dtos.dto_news import RequestAgricultureNewsDTO, ResponseAgricultureNewsDTO
from app.services.slack.channels.agriculture_news.service import alert_message

router = APIRouter(prefix="/news")


@router.post("/agriculture", response_model=ResponseAgricultureNewsDTO)
def request_agriculture_news(params: RequestAgricultureNewsDTO):
    alert_message(message="Hello World")
