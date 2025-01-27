from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Response

from finance.api.router import router as api_router
from finance.tasks.reddit.task import add_reddit_tasks

sub_routers = [
    api_router,
]

topics = ["stock"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    await add_reddit_tasks(topics=topics)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/livez")
async def liveness():
    return Response(content="liveness", status_code=200)


for sub_router in sub_routers:
    app.include_router(sub_router)
