import struct

from structure import EventNotFoundError, add_record_to_event, event, store

attributes_struct = {
    "uint64": "Q",
    "uint32": "I",
    "uint16": "H",
    "uint8": "B",
    "int64": "q",
    "int32": "i",
    "int16": "h",
    "int8": "b",
}

log_format = {"timestamp": "uint64", "event_id": "uint8", "data": "uint32"}


def build_struct_format(log_format: dict[str, str]) -> str:
    return "<" + "".join(attributes_struct[log_format[field]] for field in log_format)



def parse_log(struct_format: dict[str, str], log_format: dict[str, str], log: bytes) -> None:
    values = struct.unpack(struct_format, log)
    log = dict(zip(log_format.keys(), values))

    event_id = log["event_id"]
    timestamp = log["timestamp"]
    data = log["data"]

    if event_id in store:
        add_record_to_event(event_id, timestamp, data)
    else:
        store[event_id] = event(event_id, timestamp, data)


def parse_file(filename: str) -> None:
    struct_format = build_struct_format(log_format)
    log_size = struct.calcsize(struct_format)

    with open(filename, "rb") as f:
        while log := f.read(log_size):
            if len(log) < log_size:
                break
            try:
                parse_log(struct_format, log_format, log)
            except EventNotFoundError:
                break
