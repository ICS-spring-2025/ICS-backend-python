import copy
from ctypes import LittleEndianStructure, addressof, c_uint8, c_uint32, c_uint64, memmove, sizeof


class InstantEvent(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("timestamp", c_uint64),
        ("event_id", c_uint8),
        ("data", c_uint32),
    ]

    def to_dict(self):
        return {"timestamp": self.timestamp, "event_id": self.event_id, "data": self.data}

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f"{self.__class__.__name__}(timestamp={self.timestamp}, event_id={self.event_id}, data={self.data})"

    def __hash__(self):
        return id(self)


class _EventsIter:
    def __init__(
        self,
        lst_events,
        *,
        timestamp__gte: int = None,
        timestamp__lte: int = None,
        event_id: int = None,
    ):
        self._lst_events_iter = iter(lst_events)
        self._timestamp__gte = timestamp__gte
        self._timestamp__lte = timestamp__lte
        self._event_id = event_id

    def __next__(self):
        while True:
            instant_event = next(self._lst_events_iter)
            if instant_event.event_id == 0:
                raise StopIteration
            if self._event_id is not None and instant_event.event_id != self._event_id:
                continue
            if self._timestamp__gte is not None and instant_event.timestamp < self._timestamp__gte:
                continue
            if self._timestamp__lte is not None and instant_event.timestamp > self._timestamp__lte:
                raise StopIteration
            return instant_event


class Events:
    def __init__(self, lst_events):
        self._lst_events = lst_events
        self._timestamp__gte = None
        self._timestamp__lte = None
        self._event_id = None

    def get(self):
        return copy.copy(self)

    def filter(
        self,
        *,
        timestamp__gte: int = None,
        timestamp__lte: int = None,
        event_id: int = None,
    ):
        events = copy.copy(self)
        if event_id:
            events._event_id = event_id
        if timestamp__gte:
            events._timestamp__gte = (
                max(events._timestamp__gte, timestamp__gte) if events._timestamp__gte else timestamp__gte
            )
        if timestamp__lte:
            events._timestamp__lte = (
                min(events._timestamp__lte, timestamp__lte) if events._timestamp__lte else timestamp__lte
            )
        return events

    def __iter__(self):
        return _EventsIter(
            lst_events=self._lst_events,
            timestamp__gte=self._timestamp__gte,
            timestamp__lte=self._timestamp__lte,
            event_id=self._event_id,
        )


class _DumpIter:
    def __init__(
        self,
        filename: str,
        *,
        timestamp__gte: int = None,
        timestamp__lte: int = None,
        event_id: int = None,
    ):
        self.file = open(filename, "rb")
        self._timestamp__gte = timestamp__gte
        self._timestamp__lte = timestamp__lte
        self._event_id = event_id

    def __next__(self):
        if self.file is None:
            raise StopIteration

        while True:
            try:
                log = self.file.read(sizeof(InstantEvent))
                if not log:
                    raise StopIteration
                if len(log) < sizeof(InstantEvent):
                    raise StopIteration
                instant_event = InstantEvent()
                memmove(addressof(instant_event), log, sizeof(InstantEvent))
                if instant_event.event_id == 0:
                    raise StopIteration  # NOTE: Предполагается dump по умолчанию заполнен нулями и сбытия с id = 0 не существует
                if self._timestamp__gte is not None and instant_event.timestamp < self._timestamp__gte:
                    continue
                if self._timestamp__lte is not None and instant_event.timestamp > self._timestamp__lte:
                    continue  # NOTE: Если гарантироавнно next.timestamp >= prev.timestamp, то заменить на raise StopIteration
                return instant_event
            except EOFError:
                raise StopIteration

    def __del__(self):
        if self.file:
            self.file.close()


class Dump:
    def __init__(self):
        self._filename = None
        self._timestamp__gte = None
        self._timestamp__lte = None
        self._event_id = None

    def get_filename(self):
        return self._filename

    @staticmethod
    def get(filename):
        dump = Dump()
        dump._filename = filename
        return dump

    def get_events(self):
        lst_events = []
        for event in self:
            lst_events.append(event)
        return Events(
            lst_events=lst_events,
        ).filter(timestamp__gte=self._timestamp__gte, timestamp__lte=self._timestamp__lte, event_id=self._event_id)

    def filter(self, *, timestamp__gte: int = None, timestamp__lte: int = None, event_id: int = None):
        dump = copy.copy(self)
        if timestamp__gte:
            dump._timestamp__gte = max(dump._timestamp__gte, timestamp__gte) if dump._timestamp__gte else timestamp__gte
        if timestamp__lte:
            dump._timestamp__lte = min(dump._timestamp__lte, timestamp__lte) if dump._timestamp__lte else timestamp__lte
        if event_id:
            dump.event_id = event_id
        return dump

    def __iter__(self):
        return _DumpIter(
            filename=self._filename,
            timestamp__gte=self._timestamp__gte,
            timestamp__lte=self._timestamp__lte,
            event_id=self._event_id,
        )
