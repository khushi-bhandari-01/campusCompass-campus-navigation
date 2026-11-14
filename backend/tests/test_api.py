from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_and_map():
    assert client.get("/api/health").json() == {"status": "ok"}
    data = client.get("/api/map").json()
    assert {"nodes", "edges", "locations", "buildings"} <= set(data)
    assert len(client.get("/api/locations").json()) >= 12


def test_find_route_main_gate_to_library():
    r = client.post("/api/find-route", json={"source": "main_gate", "destination": "library"})
    assert r.status_code == 200
    body = r.json()
    assert body["success"] and body["route"][0] == "G_MAIN" and body["route"][-1] == "E_LIB"
    assert body["metrics"]["nodes_explored"] == len(body["explored"]) == len(body["trace"])
    assert body["total_cost"] > 0 and body["metrics"]["execution_time_ms"] >= 0


def test_accepts_node_ids_and_same_source_destination():
    r = client.post("/api/find-route", json={"source": "J1", "destination": "J1"}).json()
    assert r["success"] and r["route"] == ["J1"] and r["total_cost"] == 0


def test_unknown_location_returns_404():
    r = client.post("/api/find-route", json={"source": "nowhere", "destination": "library"})
    assert r.status_code == 404


def test_validation_error_and_reset():
    assert client.post("/api/find-route", json={"source": "library"}).status_code == 422
    assert client.post("/api/reset").json()["status"] == "ok"
