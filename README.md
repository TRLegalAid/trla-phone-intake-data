# trla-phone-intake-data
Mary test!
Web crawler written in Python using Selenium to get performance reports from RingCentral and add them to a Google Sheet for internal data tracking of TRLA phone calls.


## Platforms Used

Python, Selenium, Google Sheets


## Description

The script add_reports_to_google_sheet.py uses the get_reports_s.py script to automatically download the previous week's performance reports from RingCentral and add them to our [google sheet](https://docs.google.com/spreadsheets/d/14Zzlgyf7VM6ducSBYJ5fZDABLTbKiDzd5k30-pK4cUE/edit#gid=0).

* To run the task, navigate to the project directory in your command prompt and run `python add_reports_to_google_sheet.py`

**NOTE**: do not resize Google Chrome window while crawler runs!

The scripts in the ringcentral_api_code were Alex’s attempts at using RingCentral’s API to create the performance reports, but it was unclear whether this method would yield the same exact results as the performance reports from the browser. With more time one could try using this code and comparing results.

## Set up

* Install Python
* Clone this repo
* Install [chromedriver](https://chromedriver.chromium.org/downloads)
* Get the .env file
* Run `pip install -r requirements.txt` in your shell / command prompt to install necessary packages


## Notes

* Three datasets:
    * **Top level IVR:** shows how many people called in total, before selecting a path. Shows how many people selected each option.
    * **All Queues:** shows when a call HITS one of four queues -- always FROM the caller, TO the queue
    * **Calls**: shows when a call is transferred from the queue in abstract TO an actual staff person (the FROM phone number will always be the actual caller)

* What could go wrong?
    * Sometimes the wrong report gets written to Top Level IVR. You can tell that this has happened when the script writes a relatively low number of rows (less than 4000) to the spreadsheet, or if that number is lower than the number of rows for All Queues or Calls
    * Sometimes XPATHS need to be re-determined. In Chrome, I go onto RingCentral, right click an element that needs to be "clicked" by the crawler, and "Inspect" the element.  Right click on the html that pops up on the left side, select "Copy" and then XPATH (sometimes, only "Full XPATH" works).
    * Don't resize the window while crawler is crawling!

### If you need to access the RingCentral data manually:
    * Getting into RingCentral manually --
        * Go [here](https://www.ringcentral.com/)
        * Click "Login" and select "Admin Portal"
        * Sign in
        * Select "Reports"
        * Select "Analytics"
        * I typically use "Performance Reports"
        * To troubleshoot data or understand what it means, use the "Call Log" under Reports to look up a specific phone number  


### Room for Improvement

Use the API instead of Selenium, or use Selenium but have it run on Heroku  

As of now Lizzie just runs the script once per week manually

The scripts in the ringcentral_api_code were Alex’s attempts at using RingCentral’s API to create the performance reports, but it was unclear whether this method would yield the same exact results as the performance reports from the browser. With more time one could try using this code and comparing results.
