from dataclasses import dataclass
from ctypes import LittleEndianStructure, c_uint64, c_uint32, c_uint8

class InstantEvent(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("timestamp", c_uint64),
        ("event_id", c_uint8),
        ("data", c_uint32),
    ]
