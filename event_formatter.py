
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
        raise Exception("lst_possible_begins > 1")
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
        data["instant"] = event
        yield event, data


def ranged(iterator):
    started_events = set()
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
            ranged_data = {"start": started_event, "stop": event}
            data["ranged"] = ranged_data
            yield event, data
            continue
        elif _rer.get_possible_ends(event_id):
            started_events.add(event)
            yield event, data
            continue
        else:
            raise Exception(f"RangedEvent {event} don't have start and end")
    yield None, {"ranged.partial": started_events }


def ranged_extended(iterator):
    started_events = set()
    info = dict()
    for event, data in iterator:
        event_id = event.event_id
        if not event:
            yield event, data
            continue
        if event_id in _ier:
            for started_event in started_events:
                info[started_event].append(event.to_dict())
            yield event, data
            continue
        if event_id not in _rer:
            yield event, data
            continue
        elif started_event := get_started_event_for_stop_event(started_events, event_id):
            ranged_data = {"start": started_event, "stop": event, "info": info[started_event]}
            started_events.remove(started_event)
            info.pop(started_event)
            data["ranged_extended"] = ranged_data
            yield event, data
            continue
        elif _rer.get_possible_ends(event_id):
            started_events.add(event)
            info[event] = list()
            yield event, data
            continue
        else:
            raise Exception(f"RangedEvent {event} don't have start and end")
    yield None, {"ranged_extended.partial": started_events }


# to_dict(ranged(instant(wrapper(Dump(<filename>)))))
def to_dict(iterator):
    res = {
        "instant": [],
        "ranged": [],
    }
    instant_events = {}
    ranged_events = {}
    for event, data in iterator:
        if "instant" in data:
            event_id = data["instant"].event_id
            if event_id not in instant_events:
                instant_events[event_id] = list()
            instant_events[event_id].append((data["instant"].timestamp, data["instant"].data))
        elif "ranged_extended" in data:
            start_event = data["ranged_extended"]["start"]
            if start_event.event_id not in ranged_events:
                ranged_events[start_event.event_id] = list()
            ranged_events[start_event.event_id].append(
                (
                    data["ranged_extended"]["start"].timestamp,
                    data["ranged_extended"]["start"].data,
                    data["ranged_extended"]["stop"].event_id,
                    _rer.get_event_name(data["ranged_extended"]["stop"].event_id),
                    data["ranged_extended"]["stop"].timestamp,
                    data["ranged_extended"]["stop"].data,
                    data["ranged_extended"]["info"],
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
