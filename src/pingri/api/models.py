from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator


class Person(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=120)
    role: str = Field(default="member", min_length=1, max_length=40)
    groups: list[str] = Field(default_factory=list)
    responsibility: str | None = Field(default=None, max_length=200)
    telegram: str | None = Field(default=None, max_length=100)


class PersonCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    role: str = Field(default="member", min_length=1, max_length=40)
    groups: list[str] = Field(default_factory=list)
    responsibility: str | None = Field(default=None, max_length=200)
    telegram: str | None = Field(default=None, max_length=100)


class EventWorkItem(BaseModel):
    id: int
    work_type: str = Field(min_length=1, max_length=80)
    deadline: datetime
    responsible: str = Field(min_length=1, max_length=120)


class EventWorkItemCreate(BaseModel):
    work_type: str = Field(min_length=1, max_length=80)
    deadline: datetime
    responsible: str = Field(min_length=1, max_length=120)

    @field_validator("deadline")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("Укажите часовой пояс")
        return value


class Event(BaseModel):
    id: int
    title: str = Field(min_length=1, max_length=160)
    event_type: str = Field(default="Другое", min_length=1, max_length=80)
    description: str = Field(default="", max_length=2000)
    starts_at: datetime
    responsible: list[str] = Field(default_factory=list)
    group: str | None = Field(default=None, max_length=100)
    work_items: list[EventWorkItem] = Field(default_factory=list)


class EventCreate(BaseModel):
    title: str = Field(min_length=1, max_length=160)
    event_type: str = Field(default="Другое", min_length=1, max_length=80)
    description: str = Field(default="", max_length=2000)
    starts_at: datetime
    responsible: list[str] = Field(default_factory=list)
    group: str | None = Field(default=None, max_length=100)
    work_items: list[EventWorkItemCreate] = Field(default_factory=list)

    @field_validator("starts_at")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("Укажите часовой пояс")
        return value


class EventWorkloadRow(BaseModel):
    event_id: int
    event_date: datetime
    event_name: str
    event_type: str
    work_type: str
    deadline: datetime
    responsible: str


class TaskStatus(StrEnum):
    NEW = "new"
    ACCEPTED = "accepted"
    CANNOT = "cannot"
    DONE = "done"


class Task(BaseModel):
    id: int
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)
    assignee: str = Field(min_length=1, max_length=120)
    deadline: datetime
    link: str | None = Field(default=None, max_length=500)
    status: TaskStatus = TaskStatus.NEW
    comment: str | None = Field(default=None, max_length=1000)


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)
    assignee: str = Field(min_length=1, max_length=120)
    deadline: datetime
    link: str | None = Field(default=None, max_length=500)

    @field_validator("deadline")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("Укажите часовой пояс")
        return value


class TaskUpdate(BaseModel):
    status: TaskStatus
    comment: str | None = Field(default=None, max_length=1000)
