from fastapi import APIRouter

from spring.entrypoints.v1.gpt import models, service
from spring.logger import logger

router = APIRouter(prefix="/gpt")


@router.post("/query", response_model=models.ResponseGPTDTO)
def request_gpt_with_prompt(params: models.RequestGPTDTO):
    response = service.query_with_prompt(
        model="gpt-4",
        prompt=params.prompt,
    )
    message = response["choices"][0]["message"]["content"]
    logger.info(f"response: {message}")
    return response
