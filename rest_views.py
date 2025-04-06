from typing import Dict

from models import Dump
from settings import store
import event_formatter

def get_events_controller(start_time: int = None, stop_time: int = None) -> Dict:
    return event_formatter.to_dict(event_formatter.ranged(event_formatter.instant(event_formatter.wrapper(
        store.filter(
            timestamp__gte=start_time,
            timestamp__lte=stop_time
        )
    ))))

def get_event_by_id(event_id: int, start_time: int, stop_time: int) -> Dict:
    return event_formatter.to_dict(event_formatter.ranged(event_formatter.instant(event_formatter.wrapper(
        store.filter(
            event_id = event_id,
            timestamp__gte=start_time,
            timestamp__lte=stop_time,
        )
    ))))
