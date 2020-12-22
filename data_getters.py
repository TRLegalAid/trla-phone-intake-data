"""Functions to make get requests to ringcentral API and return data"""

from authenticate import login_to_platform


def get_response(endpoint, params):
    platform = login_to_platform()
    return platform.get(endpoint, params)

# date should be in format yyyy-mm-dd (ex: 2020-09-01)
def get_call_records_since(date):
    params = {"dateFrom": f"{date}T00:00:00.000Z", "perPage": "1000"}
    call_logs_response = get_response('/restapi/v1.0/account/~/extension/~/call-log', params)
    call_logs_records = call_logs_response.json().records

    # I don't think this will ever happen, but just in case
    if len(call_logs_records) > 1000:
        raise Exception("Got more than 1000 results, which means that there are multiple pages and only data from the first page is being handled.")

    print(f"Got all {len(call_logs_records)} call logs since {date}.")
    return call_logs_records

def get_todays_call_records():
    params = {"perPage": "100"}
    # dateTo, dateFrom are by default the current time and the 24 hours ago, respectively, so no need to specify those parameters
    call_logs_response = get_response('/restapi/v1.0/account/~/extension/~/call-log', params)
    call_logs_records = call_logs_response.json().records

    # I don't think this will ever happen, but just in case
    if len(call_logs_records) > 1000:
        raise Exception("Got more than 1000 results, which means that there are multiple pages and only data from the first page is being handled.")

    print(f"Got all {len(call_logs_records)} call logs from the past day.")
    return call_logs_records

# get_todays_call_records()
get_call_records_since("2020-01-01")




# resp = platform.get('/restapi/v1.0/account/~/ivr-prompts').json()
# for thing in resp.records:
#     # print(thing.uri, thing.id, thing.filename, thing.contentType)
#     print(thing.id, thing.filename)

# resp = platform.get('/restapi/v1.0/account/~/ivr-menus/149238104').json()


#
# from authenticate import login_to_platform
#
#
# platform = login_to_platform()
#
# # get list of all queues that we have
# resp = platform.get('/restapi/v1.0/account/~/call-queues')
# for thing in resp.json().records:
#     print(thing.id, thing.name, thing.extensionNumber)

# get basic info of queue with id 239704104
# resp = platform.get('/restapi/v1.0/account/~/call-queues/239704104').json()
# print(resp.id, resp.name, resp.status)

# # get members of queue with id 239704104 - can probably use these results to get the actual call data
# resp = platform.get('/restapi/v1.0/account/~/call-queues/239704104/members').json()
# for thing in resp.records:
#     print(thing.uri, thing.id, thing.extensionNumber)
#     print()
