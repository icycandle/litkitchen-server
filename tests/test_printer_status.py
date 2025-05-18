import pytest
from fastapi.testclient import TestClient
from litkitchen_server.main import app

client = TestClient(app)


def test_printer_status_api():
    r = client.get("/printer-status")
    assert r.status_code == 200
    data = r.json()
    assert "status" in data
    assert "description" in data
    # 檢查狀態與說明一致性
    if data["status"] == "ready":
        assert "就緒" in data["description"]
    if data["status"] == "out_of_paper":
        assert "缺紙" in data["description"]
    # 其他狀態可根據 PrintJobStatus 擴充


@pytest.mark.integration
def test_printer_status_integration():
    r = client.get("/printer-status")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] in [
        "queued",
        "ready",
        "printing",
        "done",
        "failed",
        "error",
        "out_of_paper",
    ]
    assert isinstance(data["description"], str)
