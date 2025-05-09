from fastapi import FastAPI

from litkitchen_server.api import router as api_router

app = FastAPI(title="litkitchen-server")

app.include_router(api_router)
