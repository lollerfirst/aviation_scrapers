import os
import sys
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import json

URL = "https://www.notams.faa.gov/dinsQueryWeb"  # Path of the page to parse.
SAVE_PATH = '/home/lollerfirst/tmp/notams-report.json'

args = sys.argv[1:]

if len(args) <= 1:
	print("Please provide a list of space-separated NOTAM tickers. Aborting...")
	exit(0)
	
tickers = {ticker: [] for ticker in args}
locId = ''
for x in args:
	locId = locId + ' ' + x
locId = locId[1:]

print('Tickers: {}'.format(args))
print('Starting Selenium webDriver')

chrome_options = webdriver.ChromeOptions()
 
#chrome_options.add_argument('--headless')  # Run Chrome in headless mode, i.e., without opening a browser window
	
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

service = Service(ChromeDriverManager().install())

print(chrome_options)

# Initialize the Chrome driver with the configured options and service
driver = webdriver.Chrome(service=service, options=chrome_options)
print("Driver started!")

# Download the page
print('Querying the page...')

driver.get(URL)

print('Page loaded! Querying tickers...')

driver.find_element('xpath', '//html//body//div[3]//div[3]//button').click()

input_form = driver.find_element(By.NAME, 'queryRetrievalForm')
text_area = input_form.find_element(By.NAME, 'retrieveLocId')
print(text_area)
text_area.send_keys(locId)

input_form.find_element(By.NAME, 'submit').click()
time.sleep(1)

print('Ticker queried. Scraping the results...')

w_handle = driver.window_handles
driver.switch_to.window(w_handle[-1])

form = driver.find_element(By.ID, 'form1')
tables = form.find_elements(By.TAG_NAME, 'table')

for i in range(0, len(args), 1):
	section = tables[3+i*2]
	
	val = args[i]
	print('Scraping for {}'.format(val))
	
	notams = section.find_elements(By.TAG_NAME, 'tr')
	
	for x in notams:
		notam = x.find_elements(By.TAG_NAME, 'td')
		if len(notam) < 2:
			continue
		
		notam = notam[1].text.replace("\n", "  ")
		#print(notam.text)
		tickers[args[i]].append(notam)


print("Saving information to {}".format(SAVE_PATH))
f = open(SAVE_PATH, "w")
f.write(json.dumps(tickers, indent=4))
f.close()
print("Bye!")
driver.quit()
