from collections.abc import Generator, Iterator
from typing import Any

from models import InstantEvent, _DumpIter
from settings import instant_event_register, ranged_event_register

_ier = instant_event_register
_rer = ranged_event_register


def wrapper(iterator: Generator[_DumpIter]) -> Generator[tuple[InstantEvent, dict[Any, Any]], None, None]:
    for event in iterator:
        yield event, {}


def instant(iterator: Generator[tuple[InstantEvent, dict]]) -> Generator[tuple[InstantEvent, dict], None, None]:
    for event, data in iterator:
        if event.event_id not in _ier:
            yield event, data
            continue
        # print(f"instant {event}, {data}")
        data["instant"] = event
        yield event, data


def ranged(iterator: Generator[tuple[InstantEvent, dict]]) -> Generator[tuple[InstantEvent, dict], None, None]:
    ranged_data = None
    started_events = set()
    ended_events = set()
    for event, data in iterator:
        if event.event_id in _rer:
            # Если у event есть possible begins, то смотрим в started_events, возмжно event является концом rangedEvent
            if possible_begins := _rer.get_possible_begins(event.event_id):
                # Список started_events, которые ожидают завершающего события с id=event_id (possible ends)
                lst_possible_begins = list(
                    filter(
                        lambda started_event: possible_begins.intersection(
                            _rer.get_possible_ends(started_event.event_id)
                        ),
                        started_events,
                    )
                )
                # Если ожидают завершения события (нашего event) больше одного, то имеет место быть наложение.
                # Время писать свой обработчик)
                if len(lst_possible_begins) > 1:
                    raise Exception(
                        "Лёня, а я говорил. Если ожидают завершения события (нашего event) больше одного, то имеет место быть наложение. Время писать свой обработчик)"
                    )
                # Завершение rangedEvent
                elif len(lst_possible_begins) == 1:
                    started_events.remove(lst_possible_begins[0])
                    ranged_data = {"start": lst_possible_begins[0], "stop": event}
                    data["ranged"] = ranged_data
                    yield event, data
                    continue
                    # Чтож... Возможно этот event является началом rangedEvent
            # Если у event есть possible ends, то добавим в started_events
            elif _rer.get_possible_ends(event.event_id):
                started_events.add(event)
                yield event, data
                continue
            # Если никто не ждёт нашего event, и у него нет possible_ends, то возможно его начало не входит в анализируемый интервал времени
            else:
                ended_events.add(event)
                yield event, data
                continue
        yield event, data


# to_dict(ranged(instant(wrapper(Dump(<filename>)))))
def to_dict(iterator: Iterator[tuple[InstantEvent, dict]]) -> dict[str, list[Any]]:
    res = {
        "instant": [],
        "ranged": [],
    }
    instant = {}
    ranged = {}
    for event, data in iterator:
        if "instant" in data:
            event_id = data["instant"].event_id
            if event_id not in instant:
                instant[event_id] = list()
            instant[event_id].append((data["instant"].timestamp, data["instant"].data))
        elif "ranged" in data:
            start_event = data["ranged"]["start"]
            if start_event.event_id not in ranged:
                ranged[start_event.event_id] = list()
            ranged[start_event.event_id].append(
                (
                    data["ranged"]["start"].timestamp,
                    data["ranged"]["start"].data,
                    data["ranged"]["stop"].event_id,
                    _rer.get_event_name(data["ranged"]["stop"].event_id),
                    data["ranged"]["stop"].timestamp,
                    data["ranged"]["stop"].data,
                )
            )
    for k, v in instant.items():
        res["instant"].append(
            {
                "id": k,
                "name": _ier.get_event_name(k),
                "records": v,
            }
        )
    for k, v in ranged.items():
        res["ranged"].append(
            {
                "id": k,
                "name": _rer.get_event_name(k),
                "records": v,
            }
        )
    return res
