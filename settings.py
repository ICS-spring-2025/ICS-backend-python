from event_registers import instant_event_register, ranged_event_register
from models import Dump, InstantEvent

instant_events = {
    128: "instant_event_128",
    129: "instant_event_129",
    130: "instant_event_130",
}
instant_event_register.register_events(instant_events)

def custom_handler_for_event131(self, instant_events: list[InstantEvent]):
    for instant_event in instant_events:
        if (self.start.timestamp <= instant_event.timestamp <= self.stop.timestamp
                and instant_event.event_id == 128):
            self.related_instant_events.append(instant_event)

ranged_event_register.register_event(131, "ranged_event_A_start", [132], custom_handler_for_event131)
ranged_event_register.register_event(132, "ranged_event_A_stop", [])
ranged_event_register.register_event(133, "ranged_event_B_start", [134, 135])
ranged_event_register.register_event(134, "ranged_event_B_stop_1", [])
ranged_event_register.register_event(135, "ranged_event_B_stop_2", [])

dump_filename = "trace_dump.bin"

store = Dump.get(dump_filename).get_events()
