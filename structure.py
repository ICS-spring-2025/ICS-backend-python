from dataclasses import dataclass

dumb_memory_path = "./trace_dump.bin"

@dataclass
class Event:
    id: int
    name: str
    records: list[tuple[float, int]]
    
store: dict[int, Event] = {}

class EventNotFoundError(Exception):
    pass

name_events = {
    1: "blocking_on_queue_peek",
    2: "blocking_on_queue_receive",
    3: "blocking_on_queue_send",
    4: "blocking_on_stream_buffer_receive",
    5: "blocking_on_stream_buffer_send",
    6: "create_counting_semaphore",
    7: "create_counting_semaphore_failed",
    8: "create_mutex",
    9: "create_mutex_failed",
    10: "event_group_clear_bits",
    11: "event_group_clear_bits_from_isr",
    12: "event_group_create",
    13: "event_group_create_failed",
    14: "event_group_delete",
    15: "event_group_set_bits",
    16: "event_group_set_bits_from_isr",
    17: "event_group_sync_block",
    18: "event_group_wait_bits_block",
    19: "free",
    20: "give_mutex_recursive",
    21: "give_mutex_recursive_failed",
    22: "increase_tick_count",
    23: "low_power_idle_begin",
    24: "low_power_idle_end",
    25: "malloc",
    26: "moved_task_to_ready_state",
    27: "pend_func_call",
    28: "pend_func_call_from_isr",
    29: "post_moved_task_to_ready_state",
    30: "queue_create",
    31: "queue_create_failed",
    32: "queue_delete",
    33: "queue_peek",
    34: "queue_peek_failed",
    35: "queue_peek_from_isr",
    36: "queue_peek_from_isr_failed",
    37: "queue_registry_add",
    38: "queue_receive",
    39: "queue_receive_failed",
    40: "queue_receive_from_isr",
    41: "queue_receive_from_isr_failed",
    42: "queue_send",
    43: "queue_send_failed",
    44: "queue_send_from_isr",
    45: "queue_send_from_isr_failed",
    46: "take_mutex_recursive",
    47: "take_mutex_recursive_failed",
    48: "task_create",
    49: "task_create_failed",
    50: "task_delay",
    51: "task_delay_until",
    52: "task_delete",
    53: "task_increment_tick",
    54: "task_notify",
    55: "task_notify_from_isr",
    56: "task_notify_give_from_isr",
    57: "task_notify_take",
    58: "task_notify_take_block",
    59: "task_notify_wait",
    60: "task_notify_wait_block",
    61: "task_priority_disinherit",
    62: "task_priority_inherit",
    63: "task_priority_set",
    64: "task_resume",
    65: "task_resume_from_isr",
    66: "task_suspend",
    67: "task_switched_in",
    68: "task_switched_out",
    69: "timer_command_received",
    70: "timer_command_send",
    71: "timer_create",
    72: "timer_create_failed",
    73: "timer_expired",
    74: "stream_buffer_create",
    75: "stream_buffer_create_failed",
    76: "stream_buffer_create_static_failed",
    77: "stream_buffer_delete",
}


def event(id: int, timestamp: float, data: int) -> Event:
    name = name_events.get(id)
    if name is None:
        raise EventNotFoundError(f"Event with id {id} not found in name_events")
    
    return Event(
        id=id,
        name=name,
        records=[(timestamp, data)]
    )
    
def add_record_to_event(id: int, timestamp:float, data: int):
    event = store.get(id)
    event.records.append((timestamp, data))
    store[id] = event
