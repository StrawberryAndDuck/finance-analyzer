from fastapi import FastAPI

from app.entrypoints.router_news import router as router_agriculture

app = FastAPI()
app.include_router(router=router_agriculture)


@app.get("/")
def home():
    ...
