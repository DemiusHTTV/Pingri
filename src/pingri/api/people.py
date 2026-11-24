from fastapi import APIRouter, HTTPException, Query

from pingri.api.models import Person, PersonCreate
from pingri.api.store import store

router = APIRouter(prefix="/api/people", tags=["Справочник"])


@router.get("", response_model=list[Person])
async def list_people(search: str | None = Query(default=None, max_length=120)) -> list[Person]:
    people = list(store.people.values())
    if search:
        needle = search.casefold()
        people = [
            person
            for person in people
            if needle in person.name.casefold()
            or needle in (person.responsibility or "").casefold()
        ]
    return sorted(people, key=lambda person: person.name.casefold())


@router.post("", response_model=Person, status_code=201)
async def add_person(data: PersonCreate) -> Person:
    person = Person(id=store.next_id("people"), **data.model_dump())
    store.people[person.id] = person
    return person


@router.delete("/{person_id}", status_code=204)
async def remove_person(person_id: int) -> None:
    if store.people.pop(person_id, None) is None:
        raise HTTPException(status_code=404, detail="Человек не найден")
