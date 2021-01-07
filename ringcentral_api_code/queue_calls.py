from data_getters import get_queues, get_user_call_records
from data_parsers import parse_call_records

queues_of_interest = ["TRLA - Receptionist - English", "TRLA - Receptionist - Spanish",
                      "TRLA - Intake - English", "TRLA - Intake - Spanish"]

# gets all calls from the past 24 hours that are associated with one of our queeus of interest
def make_queues_df():
    queues = get_queues()
    queue_ids = [queue.id for queue in queues if queue.name in queues_of_interest]
    all_call_records = []
    for queue_id in queue_ids:
        all_call_records += get_user_call_records(queue_id)

    return parse_call_records(all_call_records)
