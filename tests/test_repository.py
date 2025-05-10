import os
import tempfile
import pytest
from datetime import datetime
from litkitchen_server.infrastructure.repository_sqlite import SqliteRepository
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
    return db_path


@pytest.mark.unit
def test_crud_maindishtext(monkeypatch):
    db_path = setup_test_db(monkeypatch)
    repo = SqliteRepository(db_path)
    item = MainDishTextOrm(
        id=None,
        author_name="A",
        work_title="B",
        main_dish="C",
        publisher="D",
        genre="E",
        description="F",
    )
    created = repo.create_maindishtext(item)
    assert created.id is not None
    fetched = repo.get_maindishtext(created.id)
    assert fetched.author_name == "A"
    created.author_name = "Z"
    updated = repo.update_maindishtext(created.id, created)
    assert updated
    fetched2 = repo.get_maindishtext(created.id)
    assert fetched2.author_name == "Z"
    deleted = repo.delete_maindishtext(created.id)
    assert deleted
    assert repo.get_maindishtext(created.id) is None
    os.unlink(db_path)


@pytest.mark.unit
def test_crud_sidedishmedia(monkeypatch):
    db_path = setup_test_db(monkeypatch)
    repo = SqliteRepository(db_path)
    item = SideDishMediaOrm(id=None, media_type="movie", side_dish="side")
    created = repo.create_sidedishmedia(item)
    assert created.id is not None
    fetched = repo.get_sidedishmedia(created.id)
    assert fetched.media_type == "movie"
    created.media_type = "anime"
    updated = repo.update_sidedishmedia(created.id, created)
    assert updated
    fetched2 = repo.get_sidedishmedia(created.id)
    assert fetched2.media_type == "anime"
    deleted = repo.delete_sidedishmedia(created.id)
    assert deleted
    assert repo.get_sidedishmedia(created.id) is None
    os.unlink(db_path)


@pytest.mark.unit
def test_crud_drinkstyle(monkeypatch):
    db_path = setup_test_db(monkeypatch)
    repo = SqliteRepository(db_path)
    item = DrinkStyleOrm(id=None, style="sweet", drink="tea")
    created = repo.create_drinkstyle(item)
    assert created.id is not None
    fetched = repo.get_drinkstyle(created.id)
    assert fetched.style == "sweet"
    created.style = "bitter"
    updated = repo.update_drinkstyle(created.id, created)
    assert updated
    fetched2 = repo.get_drinkstyle(created.id)
    assert fetched2.style == "bitter"
    deleted = repo.delete_drinkstyle(created.id)
    assert deleted
    assert repo.get_drinkstyle(created.id) is None
    os.unlink(db_path)


@pytest.mark.unit
def test_crud_textvariant(monkeypatch):
    db_path = setup_test_db(monkeypatch)
    repo = SqliteRepository(db_path)
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
    created = repo.create_textvariant(item)
    assert created.id is not None
    fetched = repo.get_textvariant(created.id)
    assert fetched.content == "test"
    created.content = "updated"
    updated = repo.update_textvariant(created.id, created)
    assert updated
    fetched2 = repo.get_textvariant(created.id)
    assert fetched2.content == "updated"
    deleted = repo.delete_textvariant(created.id)
    assert deleted
    assert repo.get_textvariant(created.id) is None
    os.unlink(db_path)


@pytest.mark.unit
def test_crud_printjob(monkeypatch):
    db_path = setup_test_db(monkeypatch)
    repo = SqliteRepository(db_path)
    item = PrintJobOrm(
        id=None,
        text_variant_id=1,
        status=PrintJobStatus.queued,
        created_at=datetime.now(),
        printed_at=None,
    )
    created = repo.create_printjob(item)
    assert created.id is not None
    fetched = repo.get_printjob(created.id)
    assert fetched.status == PrintJobStatus.queued
    created.status = PrintJobStatus.done
    updated = repo.update_printjob(created.id, created)
    assert updated
    fetched2 = repo.get_printjob(created.id)
    assert fetched2.status == PrintJobStatus.done
    deleted = repo.delete_printjob(created.id)
    assert deleted
    assert repo.get_printjob(created.id) is None
    os.unlink(db_path)


@pytest.mark.unit
def test_crud_barcodemapping(monkeypatch):
    db_path = setup_test_db(monkeypatch)
    repo = SqliteRepository(db_path)
    item = BarcodeMappingOrm(
        id=None,
        barcode="abc123",
        main_dish_text_id=1,
        side_dish_media_id=2,
        drink_style_id=3,
        description="desc",
        created_at=datetime.now(),
    )
    created = repo.create_barcodemapping(item)
    assert created.id is not None
    fetched = repo.get_barcodemapping(created.id)
    assert fetched.barcode == "abc123"
    created.barcode = "def456"
    updated = repo.update_barcodemapping(created.id, created)
    assert updated
    fetched2 = repo.get_barcodemapping(created.id)
    assert fetched2.barcode == "def456"
    deleted = repo.delete_barcodemapping(created.id)
    assert deleted
    assert repo.get_barcodemapping(created.id) is None
    os.unlink(db_path)
