from typing import List, Union
from datetime import datetime
from structure import store, Event, dumb_memory_path
from parser import parse_file

def get_events(start_time: int, end_time: int) -> List[Event]:
    filtered_events = []
    parse_file(dumb_memory_path)
    for event in store.values():
        event.records = [record for record in event.records if start_time <= record[0] <= end_time]

        if event.records:
            filtered_events.append(event)
    return filtered_events


def get_event_by_id(event_id: int, start_time: int, end_time: int) -> Union[Event, None]:
    parse_file(dumb_memory_path)
    event = store.get(event_id)
    if event:
        event.records = [record for record in event.records if start_time <= record[0] <= end_time]

        if not event.records:
            print(f"No records found in the time range for event {event_id}. Returning event with empty records.")
        
        return event
    else:
        print(f"Event with ID {event_id} not found.")
    return None