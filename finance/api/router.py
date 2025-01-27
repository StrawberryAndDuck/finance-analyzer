from fastapi import APIRouter

from finance.api.v1.router import router as v1_router

sub_routers = [
    v1_router,
]

router = APIRouter(prefix="/api")

for sub_router in sub_routers:
    router.include_router(sub_router)
