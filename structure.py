from dataclasses import dataclass
from event_mappings import name_events

dumb_memory_path: str = "./trace_dump.bin"


@dataclass
class Event:
    id: int
    name: str
    records: list[tuple[float, int]]


store: dict[int, Event] = {}


class EventNotFoundError(Exception):
    pass


def event(id: int, timestamp: float, data: int) -> Event:
    name = name_events.get(id)
    if name is None:
        raise EventNotFoundError(f"Event with id {id} not found in name_events")

    return Event(
        id=id,
        name=name,
        records=[(timestamp, data)]
    )


def add_record_to_event(id: int, timestamp: float, data: int) -> None:
    event = store.get(id)
    event.records.append((timestamp, data))
    store[id] = event
