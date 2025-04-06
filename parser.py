from ctypes import sizeof, memmove, addressof

from models import InstantEvent
from structure import store, event, add_record_to_event, EventNotFoundError

def parse_log(log: bytes) -> None:
    instant_event = InstantEvent()
    memmove(addressof(instant_event), log, sizeof(InstantEvent))
    if instant_event.event_id in store:
        add_record_to_event(instant_event.event_id, instant_event.timestamp, instant_event.data)
    else:
        store[instant_event.event_id] = event(instant_event.event_id, instant_event.timestamp, instant_event.data)


def parse_file(filename: str) -> None:
    log_size = sizeof(InstantEvent)
    with open(filename, "rb") as f:
        while log := f.read(log_size):
            if len(log) < log_size:
                break
            try:
                parse_log(log)
            except EventNotFoundError as e:
                break 


