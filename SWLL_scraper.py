#NOTA DI TOM: pip install selenium webdriver-manager

import os
from io import BytesIO
from time import sleep
from PIL import Image
from urllib.request import URLopener
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

MAIN_PATH = "https://www.meteoam.it/it/swll"  # Path of the page to parse.
SAVE_FOLDER = "/home/lollerfirst/tmpimgs/"  # Folder used to save imgs.
DELAY = 5  # Seconds to wait after header creation and between subsequent trials.
MAX_RETRIES = 10

def get_page_with_retry(driver, url):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            driver.get(url)
            return
        except WebDriverException:
            print(f"Failed to load page. Retrying ({retries+1}/{max_retries})...")
            retries += 1
            time.sleep(DELAY)  # Wait for a few seconds before retrying

    # If all retries fail, raise an exception
    raise Exception(f"Failed to load page after {max_retries} retries.")

# Check if already are images in the saving folder, shows them and ask to delete.
existing_imgs = os.listdir(SAVE_FOLDER)
if len(existing_imgs) > 0:
    print('The following images already exist.\n')
    for x in existing_imgs:
        print("---> " + x)
    inp = input('Do you want to remove them? [y/n]: ')
    if inp == 'y':
        for x in existing_imgs:
            os.remove(os.path.join(SAVE_FOLDER, x))
        print('Old images removed.\n')


print("Starting Selenium driver...")
# Set Chrome options
chrome_options = webdriver.ChromeOptions()

#chrome_options.binary_location = '/media/lollerfirst/no_com/Downloads/chrome_linux/latest/chrome' 
chrome_options.add_argument('--headless')  # Run Chrome in headless mode, i.e., without opening a browser window
	
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

service = Service(ChromeDriverManager().install())

print(chrome_options)

# Initialize the Chrome driver with the configured options and service
driver = webdriver.Chrome(service=service, options=chrome_options)
print("Driver started!")


# Download the page
print('Downloading the page...\n')

get_page_with_retry(driver, MAIN_PATH)
print('Page loaded successfully. Waiting 3 seconds for scripts to load...')
time.sleep(3)



imgs = driver.find_elements(By.CSS_SELECTOR, 'img.slider-image, img.slider-side-image')
names = [img.get_attribute('src') for img in imgs]  # Used to store the path of images on the page.

    
print(names)

opener = URLopener()

# Looping over the paths of needed images to read them, open, transform into
# PIL image object and save with proper name.
for x in names:
    if x is None:
    	continue
    img = opener.open(x)
    img = img.read()
    img = Image.open(BytesIO(img))
    IMG_NAME = re.split("/Medium/|\?format", x)[1] + ".webp"

    print(IMG_NAME)
    img.save(os.path.join(SAVE_FOLDER, IMG_NAME))
    img.close()

print('Images saved correctly in ' + SAVE_FOLDER)
new_imgs = os.listdir(SAVE_FOLDER)
for img in new_imgs:
    print("---> " + img)


driver.quit()
