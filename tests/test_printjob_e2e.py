import pytest
from fastapi.testclient import TestClient
from litkitchen_server.main import app
from litkitchen_server.infrastructure.models import PrintJob
from litkitchen_server.infrastructure.repository_provider import engine, get_session
from sqlmodel import Session

# 測試共用 session
session = Session(engine)


def override_get_session():
    yield session


app.dependency_overrides[get_session] = override_get_session
client = TestClient(app)


@pytest.mark.e2e
def test_get_print_jobs(monkeypatch):
    from litkitchen_server.infrastructure.print_job_repository import PrintJobRepository

    repo = PrintJobRepository(session)
    # 清除所有資料
    for old in repo.get_all():
        repo.delete(old.id)
    # 新增一筆 fixture
    from datetime import datetime

    pj = PrintJob(
        text_variant_id=1,
        status="queued",
        created_at=datetime(2025, 1, 1, 0, 0, 0),
        printed_at=None,
    )
    created = repo.create(pj)
    resp = client.get("/print-jobs")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert any(item["id"] == created.id for item in data)
    repo.delete(created.id)


@pytest.mark.e2e
def test_post_print_job(monkeypatch):
    from litkitchen_server.infrastructure.print_job_repository import PrintJobRepository

    repo = PrintJobRepository(session)
    # 清除所有資料
    for old in repo.get_all():
        repo.delete(old.id)
    from datetime import datetime

    payload = {
        "text_variant_id": 1,
        "status": "queued",
        "created_at": datetime(2025, 1, 1, 0, 0, 0).isoformat(),
        "printed_at": None,
    }
    resp = client.post("/print-jobs", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["text_variant_id"] == 1
    repo.delete(data["id"])


@pytest.mark.e2e
def test_get_print_job_by_id(monkeypatch):
    from litkitchen_server.infrastructure.print_job_repository import PrintJobRepository

    repo = PrintJobRepository(session)
    from datetime import datetime

    pj = PrintJob(
        text_variant_id=1,
        status="queued",
        created_at=datetime(2025, 1, 1, 0, 0, 0),
        printed_at=None,
    )
    created = repo.create(pj)
    resp = client.get(f"/print-jobs/{created.id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == created.id
    repo.delete(created.id)


@pytest.mark.e2e
def test_put_print_job(monkeypatch):
    from litkitchen_server.infrastructure.print_job_repository import PrintJobRepository

    repo = PrintJobRepository(session)
    from datetime import datetime

    pj = PrintJob(
        text_variant_id=1,
        status="queued",
        created_at=datetime(2025, 1, 1, 0, 0, 0),
        printed_at=None,
    )
    created = repo.create(pj)
    from datetime import datetime

    update_payload = {
        "id": created.id,
        "text_variant_id": 1,
        "status": "printing",
        "created_at": datetime(2025, 1, 1, 0, 0, 0).isoformat(),
        "printed_at": None,
    }
    resp = client.put(f"/print-jobs/{created.id}", json=update_payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "printing"
    repo.delete(created.id)


@pytest.mark.e2e
def test_delete_print_job(monkeypatch):
    from litkitchen_server.infrastructure.print_job_repository import PrintJobRepository

    repo = PrintJobRepository(session)
    from datetime import datetime

    pj = PrintJob(
        text_variant_id=1,
        status="queued",
        created_at=datetime(2025, 1, 1, 0, 0, 0),
        printed_at=None,
    )
    created = repo.create(pj)
    resp = client.delete(f"/print-jobs/{created.id}")
    assert resp.status_code == 200
    assert resp.json()["ok"] is True
    assert repo.get(created.id) is None
