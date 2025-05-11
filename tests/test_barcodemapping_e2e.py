import pytest
from fastapi.testclient import TestClient
from litkitchen_server.main import app
from litkitchen_server.infrastructure.models import BarcodeMapping
from litkitchen_server.infrastructure.repository_provider import engine, get_session
from sqlmodel import Session

# 測試共用 session
session = Session(engine)


def override_get_session():
    yield session


app.dependency_overrides[get_session] = override_get_session
client = TestClient(app)


@pytest.mark.e2e
def test_get_barcode_mappings(monkeypatch):
    from litkitchen_server.infrastructure.barcode_mapping_repository import (
        BarcodeMappingRepository,
    )

    repo = BarcodeMappingRepository(session)
    # 清除所有資料
    for old in repo.get_all():
        repo.delete(old.id)
    # 新增一筆 fixture
    from datetime import datetime

    bm = BarcodeMapping(
        barcode="test123",
        main_dish_text_id=1,
        side_dish_media_id=2,
        drink_style_id=3,
        description="desc",
        created_at=datetime.now().isoformat(),
    )
    created = repo.create(bm)
    # Act
    resp = client.get("/barcode-mappings")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert any(item["barcode"] == "test123" for item in data)
    # Teardown
    repo.delete(created.id)


@pytest.mark.e2e
def test_post_barcode_mapping(monkeypatch):
    from litkitchen_server.infrastructure.barcode_mapping_repository import (
        BarcodeMappingRepository,
    )

    repo = BarcodeMappingRepository(session)
    # 清除所有資料
    for old in repo.get_all():
        repo.delete(old.id)
    payload = {
        "barcode": "test456",
        "main_dish_text_id": 1,
        "side_dish_media_id": 2,
        "drink_style_id": 3,
        "description": "desc",
    }
    resp = client.post("/barcode-mappings", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["barcode"] == "test456"
    # Teardown
    repo.delete(data["id"])


@pytest.mark.e2e
def test_delete_barcode_mapping(monkeypatch):
    from litkitchen_server.infrastructure.barcode_mapping_repository import (
        BarcodeMappingRepository,
    )

    repo = BarcodeMappingRepository(session)
    # 新增一筆 fixture
    from datetime import datetime

    bm = BarcodeMapping(
        barcode="test789",
        main_dish_text_id=1,
        side_dish_media_id=2,
        drink_style_id=3,
        description="desc",
        created_at=datetime.now().isoformat(),
    )
    created = repo.create(bm)
    # Act
    resp = client.delete(f"/barcode-mappings/{created.id}")
    assert resp.status_code == 200
    assert resp.json()["ok"] is True
    # 確認已刪除
    assert repo.get(created.id) is None
