from fastapi import FastAPI
from litkitchen_server.api.routers import router as api_router
from litkitchen_server import settings
import sentry_sdk
from fastapi.middleware.cors import CORSMiddleware

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    send_default_pii=settings.SENTRY_SEND_DEFAULT_PII,
)

app = FastAPI(title="litkitchen-server")

# 加入 CORS middleware 允許前端 dev server 跨域

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 啟動時插入 options fixture
try:
    from litkitchen_server.infrastructure.seed.options import insert_options_fixture

    insert_options_fixture()
except Exception as e:
    print(f"[WARN] options fixture insert failed: {e}")

app.include_router(api_router)
