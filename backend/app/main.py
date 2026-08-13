from __future__ import annotations

import sqlite3
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query, status

from .db import init_db
from .repository import (
    apply_sensor_event,
    complete_wash,
    confirm_wear,
    create_garment,
    create_outfit_event,
    get_garment,
    list_events,
    list_garments,
    list_outfit_events,
    update_care,
    update_presence,
)
from .schemas import (
    CareUpdate,
    EventLogResponse,
    GarmentCreate,
    GarmentResponse,
    OutfitEventCreate,
    OutfitEventResponse,
    PresenceUpdate,
    SensorEvent,
    WashComplete,
    WearConfirm,
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="PickFit Digital Twin API",
    version="0.1.0",
    description="Member 3 Backend / Digital Twin MVP",
    lifespan=lifespan,
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/v1/garments", response_model=GarmentResponse, status_code=status.HTTP_201_CREATED)
def register_garment(payload: GarmentCreate):
    try:
        return create_garment(payload)
    except sqlite3.IntegrityError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="garment_id or slot_id already exists") from exc


@app.get("/api/v1/garments", response_model=list[GarmentResponse])
def garments(available_only: bool = False):
    return list_garments(available_only=available_only)


@app.get("/api/v1/garments/{garment_id}", response_model=GarmentResponse)
def garment(garment_id: str):
    item = get_garment(garment_id)
    if not item:
        raise HTTPException(status_code=404, detail="Garment not found")
    return item


@app.patch("/api/v1/garments/{garment_id}/presence", response_model=GarmentResponse)
def set_presence(garment_id: str, payload: PresenceUpdate):
    item = update_presence(garment_id, payload.state, payload.source, payload.timestamp)
    if not item:
        raise HTTPException(status_code=404, detail="Garment not found")
    return item


@app.patch("/api/v1/garments/{garment_id}/care", response_model=GarmentResponse)
def set_care(garment_id: str, payload: CareUpdate):
    item = update_care(garment_id, payload.state, payload.source, payload.timestamp)
    if not item:
        raise HTTPException(status_code=404, detail="Garment not found")
    return item


@app.post("/api/v1/garments/{garment_id}/wear", response_model=GarmentResponse)
def wear(garment_id: str, payload: WearConfirm):
    item = confirm_wear(garment_id, payload.source, payload.timestamp)
    if not item:
        raise HTTPException(status_code=404, detail="Garment not found")
    return item


@app.post("/api/v1/garments/{garment_id}/wash-complete", response_model=GarmentResponse)
def wash_complete(garment_id: str, payload: WashComplete):
    item = complete_wash(garment_id, payload.source, payload.timestamp)
    if not item:
        raise HTTPException(status_code=404, detail="Garment not found")
    return item


@app.post("/api/v1/sensor-events", response_model=GarmentResponse)
def sensor_event(payload: SensorEvent):
    item = apply_sensor_event(payload)
    if not item:
        raise HTTPException(status_code=404, detail="No Garment mapped to garment_id/slot_id")
    return item


@app.post("/api/v1/outfit-events", response_model=OutfitEventResponse, status_code=status.HTTP_201_CREATED)
def add_outfit_event(payload: OutfitEventCreate):
    try:
        item, missing = create_outfit_event(payload.model_dump())
    except sqlite3.IntegrityError as exc:
        raise HTTPException(status_code=409, detail="Outfit event ID already exists") from exc
    if missing:
        raise HTTPException(status_code=422, detail={"missing_garment_ids": missing})
    assert item is not None
    return item


@app.get("/api/v1/outfit-events", response_model=list[OutfitEventResponse])
def outfit_events():
    return list_outfit_events()


@app.get("/api/v1/events", response_model=list[EventLogResponse])
def events(limit: int = Query(default=100, ge=1, le=500)):
    return list_events(limit=limit)
