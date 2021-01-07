"""Functions to transform responses into appropriate formats."""

import data_getters
import time
import pandas as pd


def parse_call_records(records):
    all_records= []
    for record in records:
        this_record, record_id = {}, record.id
        this_record["Call Record ID"] = record_id
        this_record["Session ID"] = record.sessionId
        this_record["Result"] = record.result
        this_record["Call Length"] = record.duration
        this_record["Handle Time"] = ""
        this_record["Call Start Time"] = record.startTime
        this_record["Call Direction"] = record.direction
        # some call records don't have these attributes

        try:
            this_record["telephonySessionId"] = record.telephonySessionId
        except:
            pass

        try:
            this_record["From Name"] = record.from_.name # no idea why it's from_ rather than from, but using from gives a syntax error
        except:
            pass

        try:
            this_record["From Number"] = record.from_.phoneNumber
        except:
            pass

        try:
            this_record["To Name"] = record.to.name
        except:
            pass

        try:
            this_record["To Number"] = record.to.phoneNumber
        except:
            pass

        all_records.append(this_record)

    return pd.DataFrame(all_records)
