from event_registers import instant_event_register, ranged_event_register
from models import Dump, InstantEvent
from event_mappings import init_event_mapping

dump_filename = "trace_dump_real.bin"

init_event_mapping()

store = Dump.get(dump_filename).get_events()
