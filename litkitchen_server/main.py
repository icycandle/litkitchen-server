from fastapi import FastAPI
from litkitchen_server.api.routers import router as api_router
from litkitchen_server import settings
import sentry_sdk

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    send_default_pii=settings.SENTRY_SEND_DEFAULT_PII,
)

app = FastAPI(title="litkitchen-server")

# 啟動時插入 options fixture
try:
    from litkitchen_server.infrastructure.seed.options import insert_options_fixture

    insert_options_fixture()
except Exception as e:
    print(f"[WARN] options fixture insert failed: {e}")

app.include_router(api_router)
