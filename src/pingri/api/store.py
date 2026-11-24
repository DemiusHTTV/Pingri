from datetime import datetime
from zoneinfo import ZoneInfo

from pingri.api.models import Event, Person, Task
from pingri.mock_data import MOCK_PEOPLE, mock_events, mock_tasks


class MemoryStore:
    def __init__(self) -> None:
        self.people: dict[int, Person] = {}
        self.events: dict[int, Event] = {}
        self.tasks: dict[int, Task] = {}
        self._next_ids = {"people": 1, "events": 1, "tasks": 1, "work_items": 1}
        self._mock_data_loaded = False

    def next_id(self, section: str) -> int:
        item_id = self._next_ids[section]
        self._next_ids[section] += 1
        return item_id

    def load_mock_data(self) -> None:
        if self._mock_data_loaded:
            return

        now = datetime.now(ZoneInfo("Europe/Moscow"))
        self.people = {row["id"]: Person(**row) for row in MOCK_PEOPLE}
        self.events = {row["id"]: Event(**row) for row in mock_events(now)}
        self.tasks = {row["id"]: Task(**row) for row in mock_tasks(now)}
        self._next_ids = {
            "people": max(self.people, default=0) + 1,
            "events": max(self.events, default=0) + 1,
            "tasks": max(self.tasks, default=0) + 1,
            "work_items": max(
                (item.id for event in self.events.values() for item in event.work_items),
                default=0,
            )
            + 1,
        }
        self._mock_data_loaded = True


store = MemoryStore()
