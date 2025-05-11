import pytest
from fastapi.testclient import TestClient
from litkitchen_server.main import app

client = TestClient(app)


@pytest.mark.e2e
def test_get_printer_status():
    resp = client.get("/printer-status")
    assert resp.status_code == 200
    assert "status" in resp.json()


@pytest.mark.e2e
def test_get_system_state():
    resp = client.get("/system-state")
    assert resp.status_code == 200
    assert "state" in resp.json()
    assert "last_reset" in resp.json()


@pytest.mark.e2e
def test_post_system_state_reset():
    resp = client.post("/system-state/reset")
    assert resp.status_code == 200
    assert resp.json()["ok"] is True
    assert resp.json()["state"] == "idle"
