from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


def _database_path() -> str:
    return os.getenv("SMART_WARDROBE_DB", "smart_wardrobe.db")


@contextmanager
def connection() -> Iterator[sqlite3.Connection]:
    db_path = _database_path()
    if db_path != ":memory:":
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    with connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS garments (
                id TEXT PRIMARY KEY,
                brand TEXT,
                product_name TEXT NOT NULL,
                category TEXT NOT NULL,
                color TEXT,
                material TEXT,
                size TEXT,
                wardrobe_id TEXT NOT NULL DEFAULT 'WARDROBE-01',
                slot_id TEXT UNIQUE,
                sensor_id TEXT,
                presence_state TEXT NOT NULL DEFAULT 'UNKNOWN'
                    CHECK (presence_state IN ('IN_WARDROBE', 'OUT', 'UNKNOWN')),
                care_state TEXT NOT NULL DEFAULT 'CLEAN'
                    CHECK (care_state IN ('CLEAN', 'REWEARABLE', 'NEED_WASH', 'WASHING', 'CARE_REQUIRED')),
                recommended_max_wear INTEGER NOT NULL DEFAULT 2 CHECK (recommended_max_wear >= 1),
                wear_count_since_wash INTEGER NOT NULL DEFAULT 0 CHECK (wear_count_since_wash >= 0),
                total_wear_count INTEGER NOT NULL DEFAULT 0 CHECK (total_wear_count >= 0),
                last_presence_change TEXT,
                last_worn_date TEXT,
                last_wash_date TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS event_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                garment_id TEXT,
                event_type TEXT NOT NULL,
                source TEXT NOT NULL,
                payload_json TEXT NOT NULL DEFAULT '{}',
                created_at TEXT NOT NULL,
                FOREIGN KEY (garment_id) REFERENCES garments(id) ON DELETE SET NULL
            );

            CREATE TABLE IF NOT EXISTS outfit_events (
                id TEXT PRIMARY KEY,
                top_id TEXT,
                bottom_id TEXT,
                outer_id TEXT,
                shoes_id TEXT,
                weather_json TEXT,
                purpose TEXT,
                style TEXT,
                photo_url TEXT,
                rating INTEGER CHECK (rating BETWEEN 1 AND 5),
                feedback TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (top_id) REFERENCES garments(id) ON DELETE SET NULL,
                FOREIGN KEY (bottom_id) REFERENCES garments(id) ON DELETE SET NULL,
                FOREIGN KEY (outer_id) REFERENCES garments(id) ON DELETE SET NULL,
                FOREIGN KEY (shoes_id) REFERENCES garments(id) ON DELETE SET NULL
            );

            CREATE INDEX IF NOT EXISTS idx_garments_slot_id ON garments(slot_id);
            CREATE INDEX IF NOT EXISTS idx_event_log_garment_id ON event_log(garment_id);
            CREATE INDEX IF NOT EXISTS idx_event_log_created_at ON event_log(created_at);
            CREATE INDEX IF NOT EXISTS idx_outfit_events_created_at ON outfit_events(created_at);
            """
        )
