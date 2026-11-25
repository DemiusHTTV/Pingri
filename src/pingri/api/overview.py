import csv
from io import StringIO

from fastapi import APIRouter, Query
from fastapi.responses import Response

from pingri.api.models import EventWorkloadRow
from pingri.api.store import store

router = APIRouter(prefix="/api/overview", tags=["Обзор для главных"])


@router.get("/workload", response_model=list[EventWorkloadRow])
async def event_workload(
    responsible: str | None = Query(default=None, max_length=120),
    event_type: str | None = Query(default=None, max_length=80),
) -> list[EventWorkloadRow]:
    return _workload_rows(responsible, event_type)


@router.get("/workload.csv", response_class=Response)
async def download_event_workload(
    responsible: str | None = Query(default=None, max_length=120),
    event_type: str | None = Query(default=None, max_length=80),
) -> Response:
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(
        [
            "Дата мероприятия",
            "Тип мероприятия",
            "Название мероприятия",
            "Что сделать",
            "Дедлайн",
            "ФИО ответственного",
        ]
    )
    for row in _workload_rows(responsible, event_type):
        writer.writerow(
            [
                row.event_date.strftime("%d.%m.%Y %H:%M"),
                row.event_type,
                row.event_name,
                row.work_type,
                row.deadline.strftime("%d.%m.%Y %H:%M"),
                row.responsible,
            ]
        )
    return Response(
        content="\ufeff" + output.getvalue(),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="pingri-workload.csv"'},
    )


def _workload_rows(
    responsible: str | None,
    event_type: str | None,
) -> list[EventWorkloadRow]:
    rows = []
    for event in store.events.values():
        if event_type and event.event_type.casefold() != event_type.casefold():
            continue
        for item in event.work_items:
            if responsible and item.responsible.casefold() != responsible.casefold():
                continue
            rows.append(
                EventWorkloadRow(
                    event_id=event.id,
                    event_date=event.starts_at,
                    event_name=event.title,
                    event_type=event.event_type,
                    work_type=item.work_type,
                    deadline=item.deadline,
                    responsible=item.responsible,
                )
            )
    return sorted(rows, key=lambda row: (row.event_date, row.deadline, row.responsible.casefold()))
