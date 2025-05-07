from models import InstantEvent, RangedEvent
from settings import instant_event_register, ranged_event_register

_ier = instant_event_register
_rer = ranged_event_register


def get_started_event_for_stop_event(started_events, stop_event_id):
    possible_begins = _rer.get_possible_begins(stop_event_id)
    lst_possible_begins = [
        started_event
        for started_event in started_events
        if possible_begins.intersection(_rer.get_possible_ends(started_event.event_id))
    ]
    if len(lst_possible_begins) == 0:
        return None
    if len(lst_possible_begins) > 1:
        raise Exception(f"lst_possible_begins({", ".join(lst_possible_begins)}) > 1, stop_event_id={stop_event_id}")
    return lst_possible_begins[0]


def wrapper(iterator):
    for event in iterator:
        yield event, {}


def instant(iterator):
    for event, data in iterator:
        if not event:
            yield event, data
            continue
        if event.event_id not in _ier:
            yield event, data
            continue
        # print(f"instant {event}, {data}")
        data["instant"] = InstantEvent(
            event_id=event.event_id,
            timestamp=event.timestamp,
            data=event.data,
            name=_ier.get_event_name(event.event_id),
        )
        yield event, data


def ranged(iterator):
    started_events = set()
    stoped_events = set()
    for event, data in iterator:
        event_id = event.event_id
        if not event:
            yield event, data
            continue
        if event_id not in _rer:
            yield event, data
            continue
        elif started_event := get_started_event_for_stop_event(started_events, event_id):
            started_events.remove(started_event)
            data["ranged"] = RangedEvent(
                start=started_event,
                stop=InstantEvent(
                    event_id=event.event_id,
                    timestamp=event.timestamp,
                    data=event.data,
                    name=_rer.get_event_name(event.event_id),
                )
            )
            yield event, data
            continue
        elif _rer.get_possible_ends(event_id):
            started_events.add(
                InstantEvent(
                    event_id=event.event_id,
                    timestamp=event.timestamp,
                    data=event.data,
                    name=_rer.get_event_name(event.event_id),
                )
            )
            yield event, data
            continue
        elif _rer.get_possible_begins(event_id):
            stoped_events.add(
                InstantEvent(
                    event_id=event.event_id,
                    timestamp=event.timestamp,
                    data=event.data,
                    name=_rer.get_event_name(event.event_id),
                )
            )
            continue
        else:
            raise Exception(f"RangedEvent {event} don't have start and end")
    yield None, {"ranged.partial": started_events.union(stoped_events) }


def to_arrays_by_type(iterator):
    res = {
        "instant": [],
        "ranged": [],
        "ranged.partial": []
    }
    for event, data in iterator:
        if "instant" in data:
            res["instant"].append(data["instant"])
        elif "ranged" in data:
            res["ranged"].append(data["ranged"])
        elif "ranged.partial" in data:
            res["ranged_partial_events"] = data["ranged.partial"]
    return res


def format_v1(events_by_type):
    res = {
        "instant": [],
        "ranged": [],
        "ranged.partial": []
    }

    instant_events = {}
    ranged_events = {}

    for event in events_by_type["instant"]:
        event_id = event.event_id
        if event_id not in instant_events:
            instant_events[event_id] = list()
        instant_events[event_id].append((event.timestamp, event.data))

    for event in events_by_type["ranged"]:
        if handler := _rer.get_handler(event.start.event_id):
            handler(event, events_by_type["instant"])
        else:
            event.related_instant_events_handler(events_by_type["instant"])
        start_event = event.start
        if start_event.event_id not in ranged_events:
            ranged_events[start_event.event_id] = list()
        ranged_events[start_event.event_id].append(
            (
                event.start.timestamp,
                event.start.data,
                event.stop.event_id,
                _rer.get_event_name(event.stop.event_id),
                event.stop.timestamp,
                event.stop.data,
                event.get_related_instant_events(),
            )
        )

    for k, v in instant_events.items():
        res["instant"].append(
            {
                "id": k,
                "name": _ier.get_event_name(k),
                "records": v,
            }
        )

    for k, v in ranged_events.items():
        res["ranged"].append(
            {
                "id": k,
                "name": _rer.get_event_name(k),
                "records": v,
            }
        )

    return res
