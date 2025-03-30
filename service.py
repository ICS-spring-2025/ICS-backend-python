from typing import List, Union
from structure import store, Event

def get_events(start_time: int, end_time: int) -> List[Event]:
    filtered_events = []
    for event in store.values():
        event.records = [record for record in event.records if start_time <= record[0] <= end_time]

        if event.records:
            filtered_events.append(event)
    return filtered_events


def get_event_by_id(event_id: int, start_time: int, end_time: int) -> Union[Event, None]:
    event = store.get(event_id)
    if event:
        event.records = [record for record in event.records if start_time <= record[0] <= end_time]
        return event
    return None
