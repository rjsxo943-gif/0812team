from __future__ import annotations

import json
import sqlite3
import uuid
from datetime import datetime, timezone
from typing import Any, Iterable

from .db import connection
from .schemas import CareState, GarmentCreate, PresenceState, SensorEvent, SensorEventType


def _iso(dt: datetime | None = None) -> str:
    return (dt or datetime.now(timezone.utc)).astimezone(timezone.utc).isoformat()


def _row_to_garment(row: sqlite3.Row) -> dict[str, Any]:
    data = dict(row)
    data["is_available"] = (
        data["presence_state"] == PresenceState.IN_WARDROBE.value
        and data["care_state"] in {CareState.CLEAN.value, CareState.REWEARABLE.value}
    )
    return data


def create_garment(item: GarmentCreate) -> dict[str, Any]:
    now = _iso()
    with connection() as conn:
        conn.execute(
            """
            INSERT INTO garments (
                id, brand, product_name, category, color, material, size,
                wardrobe_id, slot_id, sensor_id, presence_state, care_state,
                recommended_max_wear, created_at, updated_at, last_presence_change
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item.id,
                item.brand,
                item.product_name,
                item.category,
                item.color,
                item.material,
                item.size,
                item.wardrobe_id,
                item.slot_id,
                item.sensor_id,
                item.presence_state.value,
                item.care_state.value,
                item.recommended_max_wear,
                now,
                now,
                now,
            ),
        )
        _append_event(conn, item.id, "GARMENT_REGISTERED", "api", item.model_dump(mode="json"), now)
        row = conn.execute("SELECT * FROM garments WHERE id = ?", (item.id,)).fetchone()
        assert row is not None
        return _row_to_garment(row)


def list_garments(available_only: bool = False) -> list[dict[str, Any]]:
    with connection() as conn:
        rows = conn.execute("SELECT * FROM garments ORDER BY created_at, id").fetchall()
    result = [_row_to_garment(row) for row in rows]
    return [g for g in result if g["is_available"]] if available_only else result


def get_garment(garment_id: str) -> dict[str, Any] | None:
    with connection() as conn:
        row = conn.execute("SELECT * FROM garments WHERE id = ?", (garment_id,)).fetchone()
    return _row_to_garment(row) if row else None


def _append_event(
    conn: sqlite3.Connection,
    garment_id: str | None,
    event_type: str,
    source: str,
    payload: dict[str, Any],
    timestamp: str | None = None,
) -> None:
    conn.execute(
        """
        INSERT INTO event_log (garment_id, event_type, source, payload_json, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (garment_id, event_type, source, json.dumps(payload, ensure_ascii=False), timestamp or _iso()),
    )


def update_presence(
    garment_id: str,
    state: PresenceState,
    source: str,
    timestamp: datetime,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    ts = _iso(timestamp)
    with connection() as conn:
        existing = conn.execute("SELECT id FROM garments WHERE id = ?", (garment_id,)).fetchone()
        if not existing:
            return None
        conn.execute(
            """
            UPDATE garments
            SET presence_state = ?, last_presence_change = ?, updated_at = ?
            WHERE id = ?
            """,
            (state.value, ts, ts, garment_id),
        )
        _append_event(
            conn,
            garment_id,
            "PRESENCE_CHANGED",
            source,
            {"state": state.value, **(payload or {})},
            ts,
        )
        row = conn.execute("SELECT * FROM garments WHERE id = ?", (garment_id,)).fetchone()
        assert row is not None
        return _row_to_garment(row)


def update_care(
    garment_id: str,
    state: CareState,
    source: str,
    timestamp: datetime,
) -> dict[str, Any] | None:
    ts = _iso(timestamp)
    with connection() as conn:
        existing = conn.execute("SELECT id FROM garments WHERE id = ?", (garment_id,)).fetchone()
        if not existing:
            return None
        conn.execute(
            "UPDATE garments SET care_state = ?, updated_at = ? WHERE id = ?",
            (state.value, ts, garment_id),
        )
        _append_event(conn, garment_id, "CARE_CHANGED", source, {"state": state.value}, ts)
        row = conn.execute("SELECT * FROM garments WHERE id = ?", (garment_id,)).fetchone()
        assert row is not None
        return _row_to_garment(row)


def confirm_wear(garment_id: str, source: str, timestamp: datetime) -> dict[str, Any] | None:
    ts = _iso(timestamp)
    with connection() as conn:
        row = conn.execute("SELECT * FROM garments WHERE id = ?", (garment_id,)).fetchone()
        if not row:
            return None

        since_wash = row["wear_count_since_wash"] + 1
        total = row["total_wear_count"] + 1
        care_state = (
            CareState.NEED_WASH.value
            if since_wash >= row["recommended_max_wear"]
            else CareState.REWEARABLE.value
        )
        conn.execute(
            """
            UPDATE garments
            SET wear_count_since_wash = ?, total_wear_count = ?, last_worn_date = ?,
                care_state = ?, updated_at = ?
            WHERE id = ?
            """,
            (since_wash, total, ts, care_state, ts, garment_id),
        )
        _append_event(
            conn,
            garment_id,
            "WEAR_CONFIRMED",
            source,
            {"wear_count_since_wash": since_wash, "care_state": care_state},
            ts,
        )
        updated = conn.execute("SELECT * FROM garments WHERE id = ?", (garment_id,)).fetchone()
        assert updated is not None
        return _row_to_garment(updated)


def complete_wash(garment_id: str, source: str, timestamp: datetime) -> dict[str, Any] | None:
    ts = _iso(timestamp)
    with connection() as conn:
        exists = conn.execute("SELECT id FROM garments WHERE id = ?", (garment_id,)).fetchone()
        if not exists:
            return None
        conn.execute(
            """
            UPDATE garments
            SET care_state = ?, wear_count_since_wash = 0, last_wash_date = ?, updated_at = ?
            WHERE id = ?
            """,
            (CareState.CLEAN.value, ts, ts, garment_id),
        )
        _append_event(conn, garment_id, "WASH_COMPLETED", source, {}, ts)
        row = conn.execute("SELECT * FROM garments WHERE id = ?", (garment_id,)).fetchone()
        assert row is not None
        return _row_to_garment(row)


def resolve_garment_id(garment_id: str | None, slot_id: str | None) -> str | None:
    if garment_id:
        return garment_id if get_garment(garment_id) else None
    if not slot_id:
        return None
    with connection() as conn:
        row = conn.execute("SELECT id FROM garments WHERE slot_id = ?", (slot_id,)).fetchone()
    return row["id"] if row else None


def apply_sensor_event(event: SensorEvent) -> dict[str, Any] | None:
    garment_id = resolve_garment_id(event.garment_id, event.slot_id)
    if not garment_id:
        return None

    target_state = {
        SensorEventType.GARMENT_REMOVED: PresenceState.OUT,
        SensorEventType.GARMENT_RETURNED: PresenceState.IN_WARDROBE,
        SensorEventType.SENSOR_UNKNOWN: PresenceState.UNKNOWN,
    }[event.event_type]

    return update_presence(
        garment_id,
        target_state,
        source="sensor",
        timestamp=event.timestamp,
        payload={
            "sensor_event": event.event_type.value,
            "slot_id": event.slot_id,
            "sensor_id": event.sensor_id,
            "metadata": event.metadata,
        },
    )


def _validate_garment_ids(conn: sqlite3.Connection, garment_ids: Iterable[str | None]) -> list[str]:
    missing: list[str] = []
    for garment_id in {g for g in garment_ids if g}:
        row = conn.execute("SELECT 1 FROM garments WHERE id = ?", (garment_id,)).fetchone()
        if not row:
            missing.append(garment_id)
    return sorted(missing)


def create_outfit_event(data: dict[str, Any]) -> tuple[dict[str, Any] | None, list[str]]:
    event_id = data.get("id") or f"OUTFIT-{uuid.uuid4().hex[:12].upper()}"
    created_at = _iso(data["created_at"])
    garment_ids = [data.get("top_id"), data.get("bottom_id"), data.get("outer_id"), data.get("shoes_id")]

    with connection() as conn:
        missing = _validate_garment_ids(conn, garment_ids)
        if missing:
            return None, missing
        conn.execute(
            """
            INSERT INTO outfit_events (
                id, top_id, bottom_id, outer_id, shoes_id, weather_json,
                purpose, style, photo_url, rating, feedback, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event_id,
                data.get("top_id"),
                data.get("bottom_id"),
                data.get("outer_id"),
                data.get("shoes_id"),
                json.dumps(data.get("weather"), ensure_ascii=False) if data.get("weather") is not None else None,
                data.get("purpose"),
                data.get("style"),
                data.get("photo_url"),
                data.get("rating"),
                data.get("feedback"),
                created_at,
            ),
        )
        _append_event(
            conn,
            None,
            "OUTFIT_EVENT_CREATED",
            "api",
            {"outfit_event_id": event_id, "garment_ids": [g for g in garment_ids if g]},
            created_at,
        )
        row = conn.execute("SELECT * FROM outfit_events WHERE id = ?", (event_id,)).fetchone()
        assert row is not None
        return _row_to_outfit(row), []


def _row_to_outfit(row: sqlite3.Row) -> dict[str, Any]:
    data = dict(row)
    data["weather"] = json.loads(data.pop("weather_json")) if data["weather_json"] else None
    return data


def list_outfit_events() -> list[dict[str, Any]]:
    with connection() as conn:
        rows = conn.execute("SELECT * FROM outfit_events ORDER BY created_at DESC").fetchall()
    return [_row_to_outfit(row) for row in rows]


def list_events(limit: int = 100) -> list[dict[str, Any]]:
    with connection() as conn:
        rows = conn.execute(
            "SELECT * FROM event_log ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    result = []
    for row in rows:
        data = dict(row)
        data["payload"] = json.loads(data.pop("payload_json"))
        result.append(data)
    return result
