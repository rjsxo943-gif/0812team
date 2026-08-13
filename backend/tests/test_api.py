from __future__ import annotations

import os

os.environ["SMART_WARDROBE_DB"] = "/tmp/pickfit_test.db"

from fastapi.testclient import TestClient

from app.main import app


def setup_function():
    try:
        os.remove(os.environ["SMART_WARDROBE_DB"])
    except FileNotFoundError:
        pass


def _create_garment(client: TestClient, garment_id: str = "G0031", slot_id: str = "H07"):
    return client.post(
        "/api/v1/garments",
        json={
            "id": garment_id,
            "product_name": "Grey T-Shirt",
            "category": "TOP",
            "color": "Grey",
            "slot_id": slot_id,
            "sensor_id": f"S-{slot_id}",
            "presence_state": "IN_WARDROBE",
            "recommended_max_wear": 2,
        },
    )


def test_register_and_list_available_garment():
    with TestClient(app) as client:
        response = _create_garment(client)
        assert response.status_code == 201
        assert response.json()["is_available"] is True

        available = client.get("/api/v1/garments?available_only=true")
        assert available.status_code == 200
        assert [item["id"] for item in available.json()] == ["G0031"]


def test_sensor_event_changes_presence_without_assuming_wear():
    with TestClient(app) as client:
        _create_garment(client)

        removed = client.post(
            "/api/v1/sensor-events",
            json={"event_type": "GARMENT_REMOVED", "slot_id": "H07"},
        )
        assert removed.status_code == 200
        body = removed.json()
        assert body["presence_state"] == "OUT"
        assert body["total_wear_count"] == 0
        assert body["is_available"] is False

        events = client.get("/api/v1/events").json()
        assert any(e["event_type"] == "PRESENCE_CHANGED" for e in events)
        assert not any(e["event_type"] == "WEAR_CONFIRMED" for e in events)


def test_explicit_wear_updates_care_state():
    with TestClient(app) as client:
        _create_garment(client)

        first = client.post("/api/v1/garments/G0031/wear", json={})
        assert first.status_code == 200
        assert first.json()["care_state"] == "REWEARABLE"
        assert first.json()["wear_count_since_wash"] == 1

        second = client.post("/api/v1/garments/G0031/wear", json={})
        assert second.status_code == 200
        assert second.json()["care_state"] == "NEED_WASH"
        assert second.json()["wear_count_since_wash"] == 2
        assert second.json()["is_available"] is False

        washed = client.post("/api/v1/garments/G0031/wash-complete", json={})
        assert washed.status_code == 200
        assert washed.json()["care_state"] == "CLEAN"
        assert washed.json()["wear_count_since_wash"] == 0


def test_outfit_event_rejects_unknown_garment():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/outfit-events",
            json={"top_id": "DOES_NOT_EXIST", "rating": 5},
        )
        assert response.status_code == 422
        assert response.json()["detail"]["missing_garment_ids"] == ["DOES_NOT_EXIST"]


def test_outfit_event_is_recorded():
    with TestClient(app) as client:
        _create_garment(client)
        response = client.post(
            "/api/v1/outfit-events",
            json={
                "top_id": "G0031",
                "weather": {"temperature_c": 23, "condition": "rain"},
                "purpose": "School",
                "style": "Casual",
                "rating": 5,
                "feedback": "comfortable",
            },
        )
        assert response.status_code == 201
        assert response.json()["top_id"] == "G0031"
        assert response.json()["weather"]["temperature_c"] == 23

        items = client.get("/api/v1/outfit-events").json()
        assert len(items) == 1
        assert items[0]["rating"] == 5
