from fastapi import FastAPI, Response

from spring.entrypoints.v1.routes import v1_router

app = FastAPI()

sub_routers = [
    v1_router,
]


@app.get("/livez")
async def liveness():
    return Response(content="liveness", status_code=200)


for sub_router in sub_routers:
    app.include_router(sub_router)
