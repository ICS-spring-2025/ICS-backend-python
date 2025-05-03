from dataclasses import dataclass


class _InstantEventRegister:
    def __init__(self):
        self.__events: dict[int, str] = {}

    def register_event(self, event_id: int, name: str):
        if event_id in self.__events:
            raise ValueError(f"Event with ID {event_id} already registered.")
        self.__events[event_id] = name

    def register_events(self, events: dict[int, str]):
        for key, value in events.items():
            self.register_event(key, value)

    def __contains__(self, item):
        return item in self.__events

    def get_event_name(self, event_id: int) -> str:
        return self.__events[event_id]


class _RangedEventRegister:
    @dataclass
    class _Event:
        possible_begin_ids: set[int]
        possible_end_ids: set[int]
        name: str = None

    def __init__(self):
        self.__events: dict[int, _RangedEventRegister._Event] = dict()

    def register_event(self, event_id: int, name: str = None, possible_end_ids: list[int] = []):
        if name is None:
            raise ValueError("name cannot be None")
        if event_id in self.__events.keys() and self.__events[event_id].name is not None:
            raise ValueError(f"Event with ID {event_id} already registered.")
        if event_id in self.__events:
            self.__events[event_id].name = name
            self.__events[event_id].possible_end_ids = set(possible_end_ids)
        else:
            self.__events[event_id] = _RangedEventRegister._Event(
                name=name, possible_end_ids=set(possible_end_ids), possible_begin_ids=set()
            )
        for event_end_id in possible_end_ids:
            if event_end_id not in self.__events:
                self.__events[event_end_id] = _RangedEventRegister._Event(
                    possible_end_ids=set(), possible_begin_ids=set([event_end_id])
                )
            else:
                self.__events[event_end_id].possible_begin_ids.add(event_end_id)

    def register_events(self, events: dict[int, tuple[str, list[int]]]):
        for key, value in events.items():
            self.register_event(key, value[0], value[1])

    def __contains__(self, item):
        return item in self.__events

    def get_event_name(self, event_id: int) -> str:
        return self.__events[event_id].name

    def get_possible_ends(self, event_id: int) -> set[int]:
        return self.__events[event_id].possible_end_ids

    def get_possible_begins(self, event_id: int) -> set[int]:
        return self.__events[event_id].possible_begin_ids


instant_event_register = _InstantEventRegister()
ranged_event_register = _RangedEventRegister()
