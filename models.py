import copy
from ctypes import LittleEndianStructure, c_uint64, c_uint32, c_uint8, addressof, sizeof, memmove

class InstantEvent(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("timestamp", c_uint64),
        ("event_id", c_uint8),
        ("data", c_uint32),
    ]

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f"{self.__class__.__name__}(timestamp={self.timestamp}, event_id={self.event_id}, data={self.data})"

    def __hash__(self):
        return id(self)


class _DumpIter:
    def __init__(self, filename: str, timestamp__gte: int = None, timestamp__lte: int = None):
        self.file = open(filename, "rb")
        self.timestamp__gte = timestamp__gte
        self.timestamp__lte = timestamp__lte

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
                    raise StopIteration # NOTE: Предполагается dump по умолчанию заполнен нулями и сбытия с id = 0 не существует
                if self.timestamp__gte is not None and instant_event.timestamp < self.timestamp__gte:
                    continue
                if self.timestamp__lte is not None and instant_event.timestamp > self.timestamp__lte:
                    continue # NOTE: Если гарантироавнно next.timestamp >= prev.timestamp, то заменить на raise StopIteration
                return instant_event
            except EOFError:
                raise StopIteration

    def __del__(self):
        if self.file:
            self.file.close()

class Dump:
    """
    Example:

    dump = Dump(<filename>).filter(timestamp__gte=<start_time>, timestamp__lte=<stop_time>)
    for event in dump:
        print(event)
    """
    def __init__(self, filename: str):
        self.filename = filename
        self.timestamp__gte = None
        self.timestamp__lte = None

    def filter(self, *, timestamp__gte: int = None, timestamp__lte: int = None):
        dump = copy.copy(self)
        if timestamp__gte:
            dump.timestamp__gte = max(dump.timestamp__gte, timestamp__gte) if dump.timestamp__gte else timestamp__gte
        if timestamp__lte:
            dump.timestamp__lte = min(dump.timestamp__lte, timestamp__lte) if dump.timestamp__lte else timestamp__lte
        return dump

    def __iter__(self):
        return _DumpIter(
            filename = self.filename,
            timestamp__gte = self.timestamp__gte,
            timestamp__lte = self.timestamp__lte,
        )




