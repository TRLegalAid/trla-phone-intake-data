import os
import glob
import time
import atexit
import pandas as pd
import openpyxl
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


load_dotenv()
RINGCENTRAL_USERNAME, RINGCENTRAL_PASSWORD = os.getenv("RINGCENTRAL_USERNAME"), os.getenv("RINGCENTRAL_PASSWORD")

options = Options()
options.add_argument('--no-sandbox')
options.add_argument("window-size=1920,1080")
# options.headless = True

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

def close_driver():
    driver.close()

atexit.register(close_driver)


# returns name of most recent file in downloads, waits for download to finish
def get_latest_download_s():

    all_download = glob.glob(os.path.expanduser('~')+"/Downloads/*")
    latest_download = max(all_download, key=os.path.getmtime)

    # wait until file is downloaded
    while(latest_download[-3:] == "txt"):
            time.sleep(5)
            all_download = glob.glob(os.path.expanduser('~')+"/Downloads/*")
            latest_download = max(all_download, key=os.path.getmtime)

    print(latest_download)

    return latest_download

def open_save_excel_file(file_path):
    wb = openpyxl.load_workbook(file_path)
    wb.save(file_path)
    #check if sheet has "calls"
    if("Calls" in wb.sheetnames):
        return True
    else:
        return False


def get_reports():
    reports = {}
    driver.get("https://analytics-officeathand.att.com/performance-report/default/users")

    # make a fake download to check if real downloads have finished
    foobar_path = os.path.expanduser('~')+"/Downloads/foobar.txt"
    foobar_file = open(foobar_path,"w")
    foobar_file.close()

    authorize_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="globalId"]/div/main/div/div[1]/div[2]/button""")))
    authorize_button.click()

    email_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "credential")))
    email_field.send_keys(RINGCENTRAL_USERNAME)

    next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="pageContent"]/div/div/div/form/div/div/div/div[2]/div[2]/button""")))
    next_button.click()

    password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
    password_field.send_keys(RINGCENTRAL_PASSWORD)

    sign_in_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="pageContent"]/div/div/div/form/div/div[1]/div/div/div[3]/div/div/button[2]""")))
    sign_in_button.click()

    input("Wait for page to finish loading. If prompted, enter security code, submit it, then press enter in the terminal. Otherwise press enter in the terminal now.")

    # get english intake queue calls
    for tries in range(5):
        try:
            calls_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="globalId"]/div/main/div/div[2]/div/div[1]/div/div[3]/div""")))
            print(calls_button)
            calls_button.click()

            calendar_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="globalId"]/div/main/div/div[1]/div[2]/div/div[1]/div[1]/button/div/div/div/span""")))
            # previous xpath://*[@id="globalId"]/div/main/div/div[1]/div[2]/div/div[1]/div[1]/button/span[2]
            calendar_button.click()
            time.sleep(2)

            last_work_week_option = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """/html/body/div/div/div[2]/div[2]/div[2]/div/main/div/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div/div/div[1]/div/div[5]""")))
            last_work_week_option.click()

            done_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="globalId"]/div/main/div/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div/div[2]/div[2]/button[2]""")))
            done_button.click()

            queues_drop_down_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="select_40_value"]""")))
            queues_drop_down_button.click()
            time.sleep(2)

            trla_intake_english_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="select_4_5"]""")))
            # previous xpath: //*[@id="select_4_4"]
            # expected new xpath: //*[@id="select_2_5"]
            # //*[@id="select_2_5"]/div/div/div/div/div
            # //*[@id="select_2_4"]/div/div/div/div/div
            # try 4_5?
            trla_intake_english_button.click()

            download_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="globalId"]/div/main/div/div[1]/div[2]/div/div[2]/div[1]/div/div/button""")))
            download_button.click()

            excel_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, """excel""")))
            excel_button.click()

            latest_download = get_latest_download_s()

            has_calls = open_save_excel_file(latest_download)

            if(has_calls):
                reports["English Intake"] = pd.read_excel(latest_download, sheet_name="Calls",engine='openpyxl',converters={'Call Start Time': str, 'Handle Time':str, 'Call Length':str})
            else:
                reports["English Intake"] = pd.DataFrame()

            os.remove(latest_download)

            print("Successfully got English Intake queue calls.")

            break
        except Exception as error:
            print(f'Failed to get English Intake queue calls on try {tries + 1}.')
            if tries == 4:
                print(f"Failed to get English Intake queue calls on all 5 attempts, here's the last error message:\n{error}.")
                exit()

    # get spanish intake queue calls
    for tries in range(5):
        try:
            queues_drop_down_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="select_40_value"]""")))
            queues_drop_down_button.click()
            time.sleep(2)

            trla_intake_spanish_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="select_4_7"]""")))
            # previous xpath: //*[@id="select_4_6"]/div/div/div/div/div
            trla_intake_spanish_button.click()

            download_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="globalId"]/div/main/div/div[1]/div[2]/div/div[2]/div[1]/div/div/button""")))
            download_button.click()

            excel_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, """excel""")))
            excel_button.click()

            latest_download = get_latest_download_s()

            has_calls = open_save_excel_file(latest_download)

            if(has_calls):
                reports["Spanish Intake"] = pd.read_excel(latest_download, sheet_name="Calls",engine='openpyxl', converters={'Call Start Time': str, 'Handle Time':str, 'Call Length':str})
            else:
                reports["Spanish Intake"] = pd.DataFrame()

            os.remove(latest_download)

            print("Successfully got Spanish Intake queue calls.")
            break
        except Exception as error:
            print(f'Failed to get Spanish Intake queue calls on try {tries + 1}.')
            if tries == 4:
                print(f"Failed to get Spanish Intake queue calls on all 5 attempts, here's the last error message:\n{error}.")
                exit()

    # get english reception queue calls
    for tries in range(5):
        try:
            queues_drop_down_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="select_40_value"]""")))
            queues_drop_down_button.click()
            time.sleep(2)

            trla_reception_english_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="select_4_8"]/div/div/div/div/div""")))
            # previous xpath: //*[@id="select_4_7"]/div/div/div/div/div
            trla_reception_english_button.click()

            download_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="globalId"]/div/main/div/div[1]/div[2]/div/div[2]/div[1]/div/div/button""")))
            download_button.click()

            excel_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, """excel""")))
            excel_button.click()

            latest_download = get_latest_download_s()

            has_calls = open_save_excel_file(latest_download)

            if(has_calls):
                reports["English Reception"] = pd.read_excel(latest_download, sheet_name="Calls",engine='openpyxl', converters={'Call Start Time': str, 'Handle Time':str, 'Call Length':str})
            else:
                reports["English Reception"] = pd.DataFrame()

            os.remove(latest_download)

            print("Successfully got English Reception queue calls.")
            break
        except Exception as error:
            print(f'Failed to get English Reception queue calls on try {tries + 1}.')
            if tries == 4:
                print(f"Failed to get English Reception queue calls on all 5 attempts, here's the last error message:\n{error}.")
                #exit()

    # get spanish reception queue calls
    for tries in range(5):
        try:
            queues_drop_down_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="select_40_value"]""")))
            queues_drop_down_button.click()
            time.sleep(2)

            trla_reception_spanish_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="select_4_9"]/div/div/div/div/div""")))
            # previous xpath://*[@id="select_4_8"]/div/div/div/div/div
            trla_reception_spanish_button.click()

            download_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="globalId"]/div/main/div/div[1]/div[2]/div/div[2]/div[1]/div/div/button""")))
            download_button.click()

            excel_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, """excel""")))
            excel_button.click()
            time.sleep(5)

            latest_download = get_latest_download_s()

            has_calls = open_save_excel_file(latest_download)
            if(has_calls):
                reports["Spanish Reception"] = pd.read_excel(latest_download, sheet_name="Calls",engine='openpyxl', converters={'Call Start Time': str, 'Handle Time':str, 'Call Length':str})
            else:
                reports["Spanish Reception"] = pd.DataFrame()

            os.remove(latest_download)

            print("Successfully got Spanish Reception queue calls.")
            break
        except Exception as error:
            print(f'Failed to get Spanish Reception queue calls on try {tries + 1}.')
            if tries == 4:
                print(f"Failed to get Spanish Reception queue calls on all 5 attempts, here's the last error message:\n{error}.")
                #exit()


    time.sleep(3)
    # get Queue Calls
    for tries in range(5):
        try:
            driver.refresh()

            calendar_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="globalId"]/div/main/div/div[1]/div[2]/div/div[1]/div[1]/button/div/div/div/span""")))
            # previous xpath: //*[@id="globalId"]/div/main/div/div[1]/div[2]/div/div[1]/div[1]/button/span[2]
            calendar_button.click()
            time.sleep(2)

            last_work_week_option = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """/html/body/div/div/div[2]/div[2]/div[2]/div/main/div/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div/div/div[1]/div/div[5]""")))
            last_work_week_option.click()

            done_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="globalId"]/div/main/div/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div/div[2]/div[2]/button[2]""")))
            done_button.click()

            users_groups_depts_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """/html/body/div/div/div[2]/div[2]/div[2]/div/main/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[1]/div/div/div[2]/div/div/div/div""")))
            users_groups_depts_button.click()
            time.sleep(2)

            queues_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """/html/body/div/div/div[2]/div[2]/div[2]/div/main/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div[1]/div[1]/div/div[5]/div/div/div/div/div""")))
            queues_button.click()
            time.sleep(2)

            intake_english_checkbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """/html/body/div/div/div[2]/div[2]/div[2]/div/main/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[4]/div[2]/div/div/div/div/div""")))
            # previous xpath: /html/body/div/div/div[2]/div[2]/div[2]/div/main/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[3]/div[2]/div/div/div/div/div
            # expected xpath:  /html/body/div/div/div[2]/div[2]/portal/div/div[2]/div[3]/div/div/div[2]/div[1]/div[2]/div[2]/div/div[2]/div[4]/div[2]/div/div/div/div/div
            intake_english_checkbox.click()
            time.sleep(2)

            intake_spanish_checkbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """/html/body/div/div/div[2]/div[2]/div[2]/div/main/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[6]/div[2]/div/div/div/div/div""")))
            #previous xpath: /html/body/div/div/div[2]/div[2]/div[2]/div/main/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[5]/div[2]/div/div/div/div/div
            #expected     : /html/body/div/div/div[2]/div[2]/portal/div/div[2]/div[3]/div/div/div[2]/div[1]/div[2]/div[2]/div/div[2]/div[6]/div[2]/div/div/div/div/div
            intake_spanish_checkbox.click()
            time.sleep(2)

            reception_english_checkbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """/html/body/div/div/div[2]/div[2]/div[2]/div/main/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[7]/div[2]/div/div/div/div/div""")))
            # previously: /html/body/div/div/div[2]/div[2]/div[2]/div/main/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[6]/div[2]/div/div/div/div/div
            # expected: /html/body/div/div/div[2]/div[2]/portal/div/div[2]/div[3]/div/div/div[2]/div[1]/div[2]/div[2]/div/div[2]/div[7]/div[2]/div/div/div/div/div
            reception_english_checkbox.click()
            time.sleep(2)

            reception_spanish_checkbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """/html/body/div/div/div[2]/div[2]/div[2]/div/main/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[8]/div[2]/div/div/div/div/div""")))
            # previously: /html/body/div/div/div[2]/div[2]/div[2]/div/main/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[7]/div[2]/div/div/div/div/div
            # expected: /html/body/div/div/div[2]/div[2]/portal/div/div[2]/div[3]/div/div/div[2]/div[1]/div[2]/div[2]/div/div[2]/div[8]/div[2]/div/div/div/div/div
            reception_spanish_checkbox.click()
            time.sleep(2)

            done_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="globalId"]/div/main/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/button[2]""")))
            done_button.click()

            download_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="globalId"]/div/main/div/div[1]/div[2]/div/div[2]/div[1]/div/div/button""")))
            download_button.click()

            excel_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, """excel""")))
            excel_button.click()
            time.sleep(5)

            latest_download = get_latest_download_s()

            has_calls = open_save_excel_file(latest_download)

            if(has_calls):
                reports["Queue Calls"] = pd.read_excel(latest_download, sheet_name="Calls",engine='openpyxl', converters={'Call Start Time': str, 'Handle Time':str, 'Call Length':str})
            else:
                reports["Queue Calls"] = pd.DataFrame()


            os.remove(latest_download)

            print("Successfully got Queue calls.")
            break
        except Exception as error:
            print(f'Failed to get Queue calls on try {tries + 1}.')
            if tries == 4:
                print(f"Failed to get Queue calls on all 5 attempts, here's the last error message:\n{error}.")
                exit()

    time.sleep(3)
    # get Top Level IVR Calls
    for tries in range(5):
        try:
            driver.refresh()

            calendar_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="globalId"]/div/main/div/div[1]/div[2]/div/div[1]/div[1]/button/div/div/div/span""")))
            #previous: //*[@id="globalId"]/div/main/div/div[1]/div[2]/div/div[1]/div[1]/button/span[2]
            calendar_button.click()
            time.sleep(2)

            last_work_week_option = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """/html/body/div/div/div[2]/div[2]/div[2]/div/main/div/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div/div/div[1]/div/div[5]""")))
            last_work_week_option.click()

            done_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="globalId"]/div/main/div/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div/div[2]/div[2]/button[2]""")))
            done_button.click()

            users_groups_depts_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """/html/body/div/div/div[2]/div[2]/div[2]/div/main/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[1]/div/div/div[2]/div/div/div/div""")))
            users_groups_depts_button.click()
            time.sleep(2)

            ivr_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """/html/body/div/div/div[2]/div[2]/div[2]/div/main/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div[1]/div[1]/div/div[4]/div/div/div/div/div""")))
            ivr_button.click()
            time.sleep(2)

            main_menu_checkbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """/html/body/div/div/div[2]/div[2]/div[2]/div/main/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[4]/div[2]/div""")))
            main_menu_checkbox.click()
            time.sleep(2)

            receptionist_checkbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """/html/body/div/div/div[2]/div[2]/div[2]/div/main/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[10]/div[2]/div""")))
            # previous xpath: /html/body/div/div/div[2]/div[2]/div[2]/div/main/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[7]/div[2]/div
            # expected xpath: /html/body/div/div/div[2]/div[2]/portal/div/div[2]/div[3]/div/div/div[2]/div[1]/div[2]/div[2]/div/div[2]/div[10]/div[2]/div/div/div/div/div
            receptionist_checkbox.click()
            time.sleep(2)

            top_menu_checkbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """/html/body/div/div/div[2]/div[2]/div[2]/div/main/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[11]/div[2]""")))
            # previous: /html/body/div/div/div[2]/div[2]/div[2]/div/main/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[8]/div[2]
            # expected: /html/body/div/div/div[2]/div[2]/portal/div/div[2]/div[3]/div/div/div[2]/div[1]/div[2]/div[2]/div/div[2]/div[11]/div[2]/div/div/div/div/div
            top_menu_checkbox.click()
            time.sleep(2)

            done_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="globalId"]/div/main/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/button[2]""")))
            done_button.click()
            time.sleep(5)

            download_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="globalId"]/div/main/div/div[1]/div[2]/div/div[2]/div[1]/div/div/button""")))
            download_button.click()
            time.sleep(2)


            excel_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, """excel""")))
            excel_button.click()
            time.sleep(3)

            latest_download = get_latest_download_s()
            time.sleep(5)

            has_calls = open_save_excel_file(latest_download)
            time.sleep(5)

            if(has_calls):
                reports["IVR"] = pd.read_excel(latest_download, sheet_name="Calls",engine='openpyxl', converters={'Call Start Time': str, 'Handle Time':str, 'Call Length':str})
            else:
                reports["IVR"] = pd.DataFrame()
            time.sleep(5)


            os.remove(latest_download)

            print("Successfully got Top Level IVR calls.")
            break
        except Exception as error:
            print(f'Failed to get Top Level IVR calls on try {tries + 1}.')
            if tries == 4:
                print(f"Failed to get Top Level IVR calls on all 5 attempts, here's the last error message:\n{error}.")
                exit()

    time.sleep(5)
    input("All done - press enter and the chrome browser will close.\n")

# <<<<<<< HEAD
# =======
# >>>>>>> a8f79f9e28f8ac138b65de30f186e7cef7fff05d

    os.remove(foobar_path)

    return reports

time.sleep(5)
def combine_reports():
    reports = get_reports()
    calls_report = reports["English Intake"].append(reports["Spanish Intake"]).append(reports["English Reception"]).append(reports["Spanish Reception"])
    return {"Top Level IVR": reports["IVR"], "All Queues": reports["Queue Calls"], "Calls": calls_report}


if __name__ == '__main__':
    reports = combine_reports()
    for report in reports:
        report_data = reports[report]
        print(f"{report} has {len(report_data)} rows.")
        print(report_data.head(4))
        print("\n")
