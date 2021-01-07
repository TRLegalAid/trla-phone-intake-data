import os
import glob
import time
import atexit
import pandas as pd
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

load_dotenv()
RINGCENTRAL_USERNAME, RINGCENTRAL_PASSWORD = os.getenv("RINGCENTRAL_USERNAME"), os.getenv("RINGCENTRAL_PASSWORD")

options = Options()
options.add_argument('--no-sandbox')
options.add_argument("window-size=1920,1080")
# options.headless = True
driver = webdriver.Chrome("./chromedriver", options=options)

def close_driver():
    driver.close()

atexit.register(close_driver)


# returns name of most recent file in downloads
def get_latest_download():
    all_download = glob.glob(os.path.expanduser('~')+"/Downloads/*")
    latest_download = max(all_download, key=os.path.getmtime)
    return latest_download



def get_reports():
    reports = {}
    driver.get("https://analytics-officeathand.att.com/performance-report/default/users")

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
            calls_button.click()

            calendar_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="globalId"]/div/main/div/div[1]/div[2]/div/div[1]/button/span[2]""")))
            calendar_button.click()
            time.sleep(2)

            last_work_week_option = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, """dp_1_preset_4""")))
            last_work_week_option.click()

            done_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="globalId"]/div/main/div/div[1]/div[2]/div/div[1]/div/div[2]/div/div[2]/div[2]/button[2]""")))
            done_button.click()

            queues_drop_down_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="select_4_0_value"]""")))
            queues_drop_down_button.click()
            time.sleep(2)

            trla_intake_english_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """/html/body/div/div/div[2]/div[2]/div[2]/div/main/div/div[2]/div/div[2]/div[1]/div/div[4]/div/div/div[2]/div/div[1]/div/div[2]/div/div/div[5]""")))
            trla_intake_english_button.click()

            download_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="globalId"]/div/main/div/div[1]/div[2]/div/div[2]/div[1]/div/div/button""")))
            download_button.click()

            excel_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, """excel""")))
            excel_button.click()

            reports["English Intake"] = pd.read_excel(get_latest_download(), sheet_name="Calls")

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
            queues_drop_down_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="select_4_0_value"]""")))
            queues_drop_down_button.click()
            time.sleep(2)

            trla_intake_spanish_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """/html/body/div/div/div[2]/div[2]/div[2]/div/main/div/div[2]/div/div[2]/div[1]/div/div[4]/div/div/div[2]/div/div[1]/div/div[2]/div/div/div[7]""")))
            trla_intake_spanish_button.click()

            download_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="globalId"]/div/main/div/div[1]/div[2]/div/div[2]/div[1]/div/div/button""")))
            download_button.click()

            excel_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, """excel""")))
            excel_button.click()

            reports["Spanish Intake"] = pd.read_excel(get_latest_download(), sheet_name="Calls")

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
            queues_drop_down_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="select_4_0_value"]""")))
            queues_drop_down_button.click()
            time.sleep(2)

            trla_reception_english_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """/html/body/div/div/div[2]/div[2]/div[2]/div/main/div/div[2]/div/div[2]/div[1]/div/div[4]/div/div/div[2]/div/div[1]/div/div[2]/div/div/div[9]""")))
            trla_reception_english_button.click()

            download_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="globalId"]/div/main/div/div[1]/div[2]/div/div[2]/div[1]/div/div/button""")))
            download_button.click()

            excel_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, """excel""")))
            excel_button.click()

            reports["English Reception"] = pd.read_excel(get_latest_download(), sheet_name="Calls")

            print("Successfully got English Reception queue calls.")
            break
        except Exception as error:
            print(f'Failed to get English Reception queue calls on try {tries + 1}.')
            if tries == 4:
                print(f"Failed to get English Reception queue calls on all 5 attempts, here's the last error message:\n{error}.")
                exit()


    # get spanish reception queue calls
    for tries in range(5):
        try:
            queues_drop_down_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="select_4_0_value"]""")))
            queues_drop_down_button.click()
            time.sleep(2)

            trla_reception_spanish_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """/html/body/div/div/div[2]/div[2]/div[2]/div/main/div/div[2]/div/div[2]/div[1]/div/div[4]/div/div/div[2]/div/div[1]/div/div[2]/div/div/div[9]""")))
            trla_reception_spanish_button.click()

            download_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="globalId"]/div/main/div/div[1]/div[2]/div/div[2]/div[1]/div/div/button""")))
            download_button.click()

            excel_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, """excel""")))
            excel_button.click()

            reports["Spanish Reception"] = pd.read_excel(get_latest_download(), sheet_name="Calls")

            print("Successfully got Spanish Reception queue calls.")
            break
        except Exception as error:
            print(f'Failed to get Spanish Reception queue calls on try {tries + 1}.')
            if tries == 4:
                print(f"Failed to get Spanish Reception queue calls on all 5 attempts, here's the last error message:\n{error}.")
                exit()


    time.sleep(3)
    # get Queue Calls
    for tries in range(5):
        try:
            driver.refresh()

            calendar_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="globalId"]/div/main/div/div[1]/div[2]/div/div[1]/button/span[2]""")))
            calendar_button.click()
            time.sleep(2)

            last_work_week_option = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, """dp_1_preset_4""")))
            last_work_week_option.click()

            done_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="globalId"]/div/main/div/div[1]/div[2]/div/div[1]/div/div[2]/div/div[2]/div[2]/button[2]""")))
            done_button.click()

            users_groups_depts_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="ext_filter_1_0_value"]""")))
            users_groups_depts_button.click()

            queues_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="ext_filter_1_queues"]/div/div/div/div/div""")))
            queues_button.click()

            intake_english_checkbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """/html/body/div/div/div[2]/div[2]/div[2]/div/main/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div[3]/div/div[1]""")))
            intake_english_checkbox.click()

            intake_spanish_checkbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """/html/body/div/div/div[2]/div[2]/div[2]/div/main/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div[5]""")))
            intake_spanish_checkbox.click()

            reception_english_checkbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """/html/body/div/div/div[2]/div[2]/div[2]/div/main/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div[7]""")))
            reception_english_checkbox.click()

            reception_spanish_checkbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """/html/body/div/div/div[2]/div[2]/div[2]/div/main/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div[8]""")))
            reception_spanish_checkbox.click()

            done_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="globalId"]/div/main/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div[2]/button[2]""")))
            done_button.click()

            download_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="globalId"]/div/main/div/div[1]/div[2]/div/div[2]/div[1]/div/div/button""")))
            download_button.click()

            excel_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, """excel""")))
            excel_button.click()

            reports["Queue Calls"] = pd.read_excel(get_latest_download(), sheet_name="Calls")

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

            calendar_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="globalId"]/div/main/div/div[1]/div[2]/div/div[1]/button/span[2]""")))
            calendar_button.click()
            time.sleep(2)

            last_work_week_option = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, """dp_1_preset_4""")))
            last_work_week_option.click()

            done_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="globalId"]/div/main/div/div[1]/div[2]/div/div[1]/div/div[2]/div/div[2]/div[2]/button[2]""")))
            done_button.click()

            users_groups_depts_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="ext_filter_1_0_value"]""")))
            users_groups_depts_button.click()

            ivr_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="ext_filter_1_ivrs"]/div/div/div/div/div""")))
            ivr_button.click()

            main_menu_checkbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """/html/body/div/div/div[2]/div[2]/div[2]/div/main/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div[4]""")))
            main_menu_checkbox.click()

            receptionist_checkbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """/html/body/div/div/div[2]/div[2]/div[2]/div/main/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div[7]""")))
            receptionist_checkbox.click()

            top_menu_checkbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """/html/body/div/div/div[2]/div[2]/div[2]/div/main/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div[8]""")))
            top_menu_checkbox.click()

            done_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="globalId"]/div/main/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div[2]/button[2]""")))
            done_button.click()

            download_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="globalId"]/div/main/div/div[1]/div[2]/div/div[2]/div[1]/div/div/button""")))
            download_button.click()

            excel_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, """excel""")))
            excel_button.click()

            reports["IVR"] = pd.read_excel(get_latest_download(), sheet_name="Calls")

            print("Successfully got Top Level IVR calls.")
            break
        except Exception as error:
            print(f'Failed to get Top Level IVR calls on try {tries + 1}.')
            if tries == 4:
                print(f"Failed to get Top Level IVR calls on all 5 attempts, here's the last error message:\n{error}.")
                exit()

    time.sleep(3)
    input("All done - press enter and the chrome browser will close.\n")
    return reports

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
