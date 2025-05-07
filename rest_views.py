import event_formatter
from settings import store


def get_events_controller(start_time: int = None, stop_time: int = None) -> dict:
    return event_formatter.format_v1(event_formatter.to_arrays_by_type(
        event_formatter.ranged(
            event_formatter.instant(
                event_formatter.wrapper(store.filter(timestamp__gte=start_time, timestamp__lte=stop_time))
            )
        )
    ))


def get_event_by_id(event_id: int, start_time: int, stop_time: int) -> dict:
    return event_formatter.format_v1(event_formatter.to_arrays_by_type(
        event_formatter.ranged(
            event_formatter.instant(
                event_formatter.wrapper(
                    store.filter(
                        event_id=event_id,
                        timestamp__gte=start_time,
                        timestamp__lte=stop_time,
                    )
                )
            )
        )
    ))


def get_all_events() -> dict:
    return event_formatter.format_v1(event_formatter.to_arrays_by_type(
        event_formatter.ranged(event_formatter.instant(event_formatter.wrapper(store.get())))
    ))
