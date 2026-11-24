from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Query

from pingri.api.models import Event, EventCreate, EventWorkItem
from pingri.api.store import store

router = APIRouter(prefix="/api/events", tags=["Мероприятия"])


@router.get("", response_model=list[Event])
async def list_events(
    days: int = Query(default=14, ge=1, le=90),
) -> list[Event]:
    now = datetime.now(timezone.utc)
    until = now.timestamp() + days * 86400
    items = [
        event
        for event in store.events.values()
        if now.timestamp() <= event.starts_at.timestamp() <= until
    ]
    return sorted(items, key=lambda event: event.starts_at)


@router.post("", response_model=Event, status_code=201)
async def add_event(data: EventCreate) -> Event:
    fields = data.model_dump(exclude={"work_items"})
    work_items = [
        EventWorkItem(id=store.next_id("work_items"), **item.model_dump())
        for item in data.work_items
    ]
    event = Event(
        id=store.next_id("events"),
        work_items=work_items,
        **fields,
    )
    store.events[event.id] = event
    return event


@router.delete("/{event_id}", status_code=204)
async def remove_event(event_id: int) -> None:
    if store.events.pop(event_id, None) is None:
        raise HTTPException(status_code=404, detail="Мероприятие не найдено")
