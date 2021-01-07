from data_getters import get_call_records_since
from data_parsers import parse_call_records

ivrs_of_interest = ["TRLA - Top Menu", "TRLA - Receptionist", "TRLA - Intake - Main Menu", "TRLA - Receptionist - English",
                    "TRLA - Receptionist - Spanish", "TRLA - Receptionist - English - ", "TRLA - Receptionist - English - WIRELESS CALLER",
                    "TRLA - Receptionist - Spanish - WIRELESS CALLER", "TRLA - Receptionist - Spanish - "]

# gets all call log legs from the last day that is two or from one of our ivrs of interests
def make_ivrs_df():
    call_logs = get_call_records_since(get_todays_records=True, view="Detailed")
    call_records = []
    for call_log in call_logs:
        legs = call_log.legs
        for leg in legs:
            try:
                to_name = leg.to.name
            except:
                to_name = ""

            try:
                from_name = leg.from_.name
            except:
                from_name = ""

            # if (to_name in ivrs_of_interest) or (from_name in ivrs_of_interest) or ("top menu" in to_name.lower()) or ("top menu" in from_name.lower()) or ("receptionist" in to_name.lower()) or ("receptionist" in from_name.lower()) or ("main menu" in to_name.lower()) or ("main menu" in from_name.lower()):
            if (to_name in ivrs_of_interest) or (from_name in ivrs_of_interest):
                leg.id = call_log.id
                leg.sessionId = call_log.sessionId
                call_records.append(leg)
            elif ("top menu" in to_name.lower()) or ("top menu" in from_name.lower()) or ("receptionist" in to_name.lower()) or ("receptionist" in from_name.lower()) or ("main menu" in to_name.lower()) or ("main menu" in from_name.lower()):
                print(to_name)
                print(from_name)
                print("\n")

    return parse_call_records(call_records)
