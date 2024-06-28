from fastapi import APIRouter

from spring.entrypoints.v1.gpt.endpoints import router as gpt_router

sub_routers = [
    gpt_router,
]

router = APIRouter(prefix="/v1")

for sub_router in sub_routers:
    router.include_router(sub_router)
