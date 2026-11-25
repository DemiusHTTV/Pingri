from fastapi import APIRouter, HTTPException, Query

from pingri.api.models import Task, TaskCreate, TaskStatus, TaskUpdate
from pingri.api.store import store

router = APIRouter(prefix="/api/tasks", tags=["Задачи"])


@router.get("", response_model=list[Task])
async def list_tasks(
    assignee: str | None = Query(default=None, max_length=120),
) -> list[Task]:
    items = list(store.tasks.values())
    if assignee:
        items = [task for task in items if task.assignee.casefold() == assignee.casefold()]
    return sorted(items, key=lambda task: task.deadline)


@router.post("", response_model=Task, status_code=201)
async def add_task(data: TaskCreate) -> Task:
    task = Task(id=store.next_id("tasks"), **data.model_dump())
    store.tasks[task.id] = task
    return task


@router.patch("/{task_id}", response_model=Task)
async def update_task(task_id: int, data: TaskUpdate) -> Task:
    task = store.tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    if data.status == TaskStatus.CANNOT and not (data.comment or "").strip():
        raise HTTPException(status_code=422, detail="Напишите, почему не получается")
    updated = task.model_copy(update=data.model_dump())
    store.tasks[task_id] = updated
    return updated


@router.delete("/{task_id}", status_code=204)
async def remove_task(task_id: int) -> None:
    if store.tasks.pop(task_id, None) is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
