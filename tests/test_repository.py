import os
import tempfile
import pytest
from datetime import datetime
from litkitchen_server.infrastructure.repository_sqlite import init_db
from sqlmodel import Session, create_engine
from litkitchen_server.infrastructure.models import (
    MainDishTextOrm,
    SideDishMediaOrm,
    DrinkStyleOrm,
    TextVariantOrm,
    PrintJobOrm,
    BarcodeMappingOrm,
)
from litkitchen_server.domain.models import PrintJobStatus

_tmp_dirs = []


def setup_test_db(monkeypatch):
    # 建立暫存 DB 與 schema.sql 複本於同一暫存目錄
    tmp_dir = tempfile.TemporaryDirectory()
    _tmp_dirs.append(tmp_dir)  # 避免被垃圾回收提前刪除
    db_path = os.path.join(tmp_dir.name, "test.sqlite3")
    # 確保 DB 檔案存在
    with open(db_path, "w"):
        pass
    schema_src = os.path.join(os.path.dirname(__file__), "../sql/schema.sql")
    schema_dst_dir = os.path.join(tmp_dir.name, "sql")
    os.makedirs(schema_dst_dir, exist_ok=True)
    schema_dst = os.path.join(schema_dst_dir, "schema.sql")
    import shutil

    shutil.copy(schema_src, schema_dst)
    # monkeypatch schema 路徑與 DB 路徑
    monkeypatch.setenv("LITKITCHEN_DB_PATH", db_path)
    monkeypatch.setenv("LITKITCHEN_SCHEMA_PATH", schema_dst)
    # 關鍵：import models 來註冊所有 ORM
    engine = create_engine(f"sqlite:///{db_path}", echo=False)
    init_db(engine)
    return engine


@pytest.mark.unit
def test_crud_maindishtext(monkeypatch):
    engine = setup_test_db(monkeypatch)
    from litkitchen_server.infrastructure.main_dish_text_repository import (
        MainDishTextRepository,
    )

    with Session(engine) as session:
        repo = MainDishTextRepository(session)
        item = MainDishTextOrm(
            id=None,
            author_name="A",
            work_title="B",
            main_dish="C",
            publisher="D",
            genre="E",
            description="F",
        )
        created = repo.create(item)
        assert created.id is not None
        fetched = repo.get(created.id)
        assert fetched.author_name == "A"
        created.author_name = "Z"
        updated = repo.update(created.id, created)
        assert updated
        fetched2 = repo.get(created.id)
        assert fetched2.author_name == "Z"
        deleted = repo.delete(created.id)
        assert deleted
        assert repo.get(created.id) is None


@pytest.mark.unit
def test_crud_sidedishmedia(monkeypatch):
    engine = setup_test_db(monkeypatch)
    from litkitchen_server.infrastructure.side_dish_media_repository import (
        SideDishMediaRepository,
    )

    with Session(engine) as session:
        repo = SideDishMediaRepository(session)
        item = SideDishMediaOrm(id=None, media_type="movie", side_dish="side")
        created = repo.create(item)
        assert created.id is not None
        fetched = repo.get(created.id)
        assert fetched.media_type == "movie"
        created.media_type = "anime"
        updated = repo.update(created.id, created)
        assert updated
        fetched2 = repo.get(created.id)
        assert fetched2.media_type == "anime"
        deleted = repo.delete(created.id)
        assert deleted
        assert repo.get(created.id) is None


@pytest.mark.unit
def test_crud_drinkstyle(monkeypatch):
    engine = setup_test_db(monkeypatch)
    from litkitchen_server.infrastructure.drink_style_repository import (
        DrinkStyleRepository,
    )

    with Session(engine) as session:
        repo = DrinkStyleRepository(session)
        item = DrinkStyleOrm(id=None, style="sweet", drink="tea")
        created = repo.create(item)
        assert created.id is not None
        fetched = repo.get(created.id)
        assert fetched.style == "sweet"
        created.style = "bitter"
        updated = repo.update(created.id, created)
        assert updated
        fetched2 = repo.get(created.id)
        assert fetched2.style == "bitter"
        deleted = repo.delete(created.id)
        assert deleted
        assert repo.get(created.id) is None


@pytest.mark.unit
def test_crud_textvariant(monkeypatch):
    engine = setup_test_db(monkeypatch)
    from litkitchen_server.infrastructure.text_variant_repository import (
        TextVariantRepository,
    )

    with Session(engine) as session:
        repo = TextVariantRepository(session)
        item = TextVariantOrm(
            id=None,
            main_dish_text_id=1,
            side_dish_media_id=2,
            drink_style_id=3,
            content="test",
            variant_index=0,
            length=10,
            approved=True,
            created_at=datetime.now(),
            print_count=1,
        )
        created = repo.create(item)
        assert created.id is not None
        fetched = repo.get(created.id)
        assert fetched.content == "test"
        created.content = "updated"
        updated = repo.update(created.id, created)
        assert updated
        fetched2 = repo.get(created.id)
        assert fetched2.content == "updated"
        deleted = repo.delete(created.id)
        assert deleted
        assert repo.get(created.id) is None


@pytest.mark.unit
def test_crud_printjob(monkeypatch):
    engine = setup_test_db(monkeypatch)
    from litkitchen_server.infrastructure.print_job_repository import PrintJobRepository

    with Session(engine) as session:
        repo = PrintJobRepository(session)
        item = PrintJobOrm(
            id=None,
            text_variant_id=1,
            status=PrintJobStatus.queued,
            created_at=datetime.now(),
        )
        created = repo.create(item)
        assert created.id is not None
        fetched = repo.get(created.id)
        assert fetched.status == PrintJobStatus.queued
        created.status = PrintJobStatus.done
        updated = repo.update(created.id, created)
        assert updated
        fetched2 = repo.get(created.id)
        assert fetched2.status == PrintJobStatus.done
        deleted = repo.delete(created.id)
        assert deleted
        assert repo.get(created.id) is None


@pytest.mark.unit
def test_crud_barcodemapping(monkeypatch):
    engine = setup_test_db(monkeypatch)
    from litkitchen_server.infrastructure.barcode_mapping_repository import (
        BarcodeMappingRepository,
    )

    with Session(engine) as session:
        repo = BarcodeMappingRepository(session)
        item = BarcodeMappingOrm(
            id=None,
            barcode="abc123",
            main_dish_text_id=1,
            side_dish_media_id=2,
            drink_style_id=3,
            description="desc",
            created_at=datetime.now(),
        )
        created = repo.create(item)
        assert created.id is not None
        fetched = repo.get(created.id)
        assert fetched.barcode == "abc123"
        created.barcode = "def456"
        updated = repo.update(created.id, created)
        assert updated
        fetched2 = repo.get(created.id)
        assert fetched2.barcode == "def456"
        deleted = repo.delete(created.id)
        assert deleted
        assert repo.get(created.id) is None
