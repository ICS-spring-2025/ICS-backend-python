from event_registers import instant_event_register, ranged_event_register

instant_events = {
    128: "instant_event_128",
    129: "instant_event_129",
    130: "instant_event_130",
}

ranged_events = {
    131: ("ranged_event_A_start", [132]),
    132: ("ranged_event_A_stop", []),
    133: ("ranged_event_B_start", [134, 135]),
    134: ("ranged_event_B_stop_1", []),
    135: ("ranged_event_B_stop_2", []),
}

instant_event_register.register_events(instant_events)
ranged_event_register.register_events(ranged_events)

dump_filename = "trace_dump.bin"
