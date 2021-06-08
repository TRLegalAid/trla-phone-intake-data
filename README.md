# trla-phone-intake-data
Web crawler written in Python using Selenium to get performance reports from RingCentral and add them to a Google Sheet for internal data tracking of TRLA phone calls.


## Platforms Used 

Python, Selenium, Google Sheets 

## Description/Notes 

The script add_reports_to_google_sheet.py uses the get_reports_s.py script to automatically download the performance reports and add them to our google sheet. 

Requires chromedriver installation. 

To run the task, use python add_reports_to_google_sheet.py 

The scripts in the ringcentral_api_code were Alex’s attempts at using RingCentral’s API to create the performance reports, but it was unclear whether this method would yield the same exact results as the performance reports from the browser. With more time one could try using this code and comparing results. 

## Room for Improvement 

Use the API instead of Selenium, or use Selenium but have it run on Heroku  

As of now Lizzie just runs the script once per week manually 
