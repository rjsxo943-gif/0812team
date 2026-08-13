from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, model_validator


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class PresenceState(str, Enum):
    IN_WARDROBE = "IN_WARDROBE"
    OUT = "OUT"
    UNKNOWN = "UNKNOWN"


class CareState(str, Enum):
    CLEAN = "CLEAN"
    REWEARABLE = "REWEARABLE"
    NEED_WASH = "NEED_WASH"
    WASHING = "WASHING"
    CARE_REQUIRED = "CARE_REQUIRED"


class SensorEventType(str, Enum):
    GARMENT_REMOVED = "GARMENT_REMOVED"
    GARMENT_RETURNED = "GARMENT_RETURNED"
    SENSOR_UNKNOWN = "SENSOR_UNKNOWN"


class GarmentCreate(BaseModel):
    id: str = Field(pattern=r"^[A-Za-z0-9_-]+$", min_length=1, max_length=64)
    product_name: str = Field(min_length=1, max_length=200)
    category: str = Field(min_length=1, max_length=100)
    brand: str | None = None
    color: str | None = None
    material: str | None = None
    size: str | None = None
    wardrobe_id: str = "WARDROBE-01"
    slot_id: str | None = None
    sensor_id: str | None = None
    presence_state: PresenceState = PresenceState.UNKNOWN
    care_state: CareState = CareState.CLEAN
    recommended_max_wear: int = Field(default=2, ge=1, le=100)


class GarmentResponse(BaseModel):
    id: str
    product_name: str
    category: str
    brand: str | None
    color: str | None
    material: str | None
    size: str | None
    wardrobe_id: str
    slot_id: str | None
    sensor_id: str | None
    presence_state: PresenceState
    care_state: CareState
    recommended_max_wear: int
    wear_count_since_wash: int
    total_wear_count: int
    last_presence_change: datetime | None
    last_worn_date: datetime | None
    last_wash_date: datetime | None
    created_at: datetime
    updated_at: datetime
    is_available: bool


class PresenceUpdate(BaseModel):
    state: PresenceState
    source: str = "manual"
    timestamp: datetime = Field(default_factory=utc_now)


class CareUpdate(BaseModel):
    state: CareState
    source: str = "manual"
    timestamp: datetime = Field(default_factory=utc_now)


class WearConfirm(BaseModel):
    source: str = "user"
    timestamp: datetime = Field(default_factory=utc_now)


class WashComplete(BaseModel):
    source: str = "user"
    timestamp: datetime = Field(default_factory=utc_now)


class SensorEvent(BaseModel):
    event_type: SensorEventType
    garment_id: str | None = None
    slot_id: str | None = None
    sensor_id: str | None = None
    timestamp: datetime = Field(default_factory=utc_now)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def require_identity(self) -> "SensorEvent":
        if not self.garment_id and not self.slot_id:
            raise ValueError("garment_id or slot_id is required")
        return self


class OutfitEventCreate(BaseModel):
    id: str | None = None
    top_id: str | None = None
    bottom_id: str | None = None
    outer_id: str | None = None
    shoes_id: str | None = None
    weather: dict[str, Any] | None = None
    purpose: str | None = None
    style: str | None = None
    photo_url: str | None = None
    rating: int | None = Field(default=None, ge=1, le=5)
    feedback: str | None = None
    created_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def at_least_one_garment(self) -> "OutfitEventCreate":
        if not any([self.top_id, self.bottom_id, self.outer_id, self.shoes_id]):
            raise ValueError("at least one garment_id is required")
        return self


class OutfitEventResponse(BaseModel):
    id: str
    top_id: str | None
    bottom_id: str | None
    outer_id: str | None
    shoes_id: str | None
    weather: dict[str, Any] | None
    purpose: str | None
    style: str | None
    photo_url: str | None
    rating: int | None
    feedback: str | None
    created_at: datetime


class EventLogResponse(BaseModel):
    id: int
    garment_id: str | None
    event_type: str
    source: str
    payload: dict[str, Any]
    created_at: datetime
