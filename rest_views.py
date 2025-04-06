from typing import Dict

from models import Dump
from settings import dump_filename
import event_formatter

def get_events_controller(start_time: int = None, stop_time: int = None) -> Dict:
    return event_formatter.to_dict(event_formatter.ranged(event_formatter.instant(event_formatter.wrapper(
        Dump(dump_filename).filter(
            timestamp__gte=start_time,
            timestamp__lte=stop_time
        )
    ))))
