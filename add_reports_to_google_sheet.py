import os
import gspread
import pandas as pd
import simplejson as json
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
from get_reports_s import combine_reports

load_dotenv()

# returns a client to use for accessing our google sheet
def init_sheets():
    json_creds = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
    creds_dict = json.loads(json_creds)
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\\\n", "\n")
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict)
    client = gspread.authorize(creds)
    return client

# opens the sheet sheet_name from the file file_name using client - returns the opened sheet object
def open_sheet(client, file_name="", sheet_name=""):
    sheet = client.open(file_name).worksheet(sheet_name)
    return sheet

# writes a pandas dataframe to sheet
def write_dataframe(sheet, df):
    df.fillna("", inplace=True)
    sheet.update([df.columns.values.tolist()] + df.values.tolist())
    print(f"Wrote new full report to {sheet}.")

# read data from sheet into dataframe
def read_data(sheet):
    df = pd.DataFrame(sheet.get_all_records())
    return df

# clears all values in sheet
def clear_sheet(sheet):
    sheet.clear()

# replaces data in sheet with the dataframe df
def replace_sheet_with_df(df, sheet):
    clear_sheet(sheet)
    write_dataframe(sheet, df)

# replaces data in sheet named sheet_name with data in the dataframe new_report
def add_new_report_to_google_sheet(sheet_name, new_report):
    print(f"Will add {len(new_report)} rows to {sheet_name}.")
    sheet = open_sheet(init_sheets(), file_name="RingCentral and Intake Tracker", sheet_name=sheet_name)
    sheet_data = read_data(sheet)
    full_report = sheet_data.append(new_report)
    write_dataframe(sheet, full_report)

# adds all three new reports to our google sheet
def add_new_reports_to_google_sheet():
    new_reports = combine_reports()
    for new_report_name in new_reports:
        new_report = new_reports[new_report_name]
        add_new_report_to_google_sheet(new_report_name, new_report)


if __name__ == '__main__':
    add_new_reports_to_google_sheet()
