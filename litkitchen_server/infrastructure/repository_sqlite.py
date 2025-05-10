import os
from sqlmodel import SQLModel, create_engine

DB_PATH = os.environ.get(
    "LITKITCHEN_DB_PATH", os.path.join(os.path.dirname(__file__), "../db.sqlite3")
)
DATABASE_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(DATABASE_URL, echo=False)


def init_db(engine_=None):
    """
    初始化資料庫 schema，使用 SQLModel 的 metadata.create_all。
    engine_ 可選，預設為 None，若給定則用該 engine。
    """
    target_engine = engine_ if engine_ is not None else engine
    SQLModel.metadata.create_all(target_engine)
