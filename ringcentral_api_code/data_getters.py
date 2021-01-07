"""Functions to make get requests to ringcentral API and return data"""

from authenticate import login_to_platform
import time


def get_response(endpoint, params):
    platform = login_to_platform()
    return platform.get(endpoint, params)

# date should be in format yyyy-mm-dd (ex: 2020-09-01)
# returns a list of json objects, each of which is one call log record
def get_call_records_since(date="", get_todays_records=False, view="Simple"):
    if get_todays_records:
        # no need to specify dateFrom because it's 24 hours ago by default
        params = {"perPage": "1000", "view": view}

    else:
        params = {"dateFrom": f"{date}T00:00:00.000Z", "perPage": "1000", "view": view}


    call_logs_response = get_response('/restapi/v1.0/account/~/call-log', params).json()
    call_logs_records = call_logs_response.records

    current_records = call_logs_response.records
    while len(current_records) >= 1000:
        next_page_uri = call_logs_response.navigation.nextPage.uri
        next_page_response = get_response(next_page_uri, params).json()
        call_logs_response, current_records = next_page_response, next_page_response.records
        call_logs_records += current_records
        time.sleep(5)

    if get_todays_records:
        print(f"Got all {len(call_logs_records)} call logs from the past 24 hours.")
    else:
        print(f"Got all {len(call_logs_records)} call logs since {date}.")
        
    return call_logs_records

# gets all call records for user with id user_id between current time and 24 hours ago
def get_user_call_records(user_id):
    params = {"perPage": "1000"}
    call_logs_response = get_response(f'/restapi/v1.0/account/~/extension/{user_id}/call-log', params).json()
    call_logs_records = call_logs_response.records

    current_records = call_logs_response.records
    while len(current_records) >= 1000:
        next_page_uri = call_logs_response.navigation.nextPage.uri
        next_page_response = get_response(next_page_uri, params).json()
        call_logs_response, current_records = next_page_response, next_page_response.records
        call_logs_records += current_records
        time.sleep(5)

    print(f"Got all {len(call_logs_records)} call logs from the past 24 hours for user {user_id}.")
    return call_logs_records

# get info regarding each queue
def get_queues():
    return get_response('/restapi/v1.0/account/~/call-queues', {}).json().records
