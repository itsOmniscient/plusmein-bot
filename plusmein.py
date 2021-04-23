from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import time
import re
import sys
import os
from dotenv import load_dotenv
from pathlib import Path

print("The bot is starting, please wait...")

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
firefox_path = os.getenv("FIREFOX")
instagram_username = os.getenv("INSTAGRAM_USERNAME")

options = Options()
options.add_argument("--headless")
fp = webdriver.FirefoxProfile(firefox_path)
driver = webdriver.Firefox(fp, options=options)

def wait():
    WebDriverWait(driver, 30).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

retry = 0
success = False
attempt = 0
print("Please wait, this process can take a couple of minutes...")
while retry <= 10:
    driver.get("https://plusmein.com/index.php?page=addfreefollowers")
    wait()
    try:
        driver.find_element_by_xpath('//*[@id="header2"]/header/div/div/div/a[2]').click()
        wait()
        website_username_id = driver.find_element_by_id('username')
        website_username_id.send_keys(instagram_username)
        time.sleep(1)
        driver.find_element_by_id('targetuser').click()
        time.sleep(4)
        driver.find_element_by_id('formcartbutton').click()
    except:
        success = False
    wait()
    try:
        insta_clock_element = driver.find_element_by_xpath('//*[@id="clock"]')
        insta_clock_element_text = insta_clock_element.text
        reg = re.compile('[0-9]*[:][0-9]*[:][0-9]*')
        insta_clock_time_list = reg.findall(insta_clock_element_text)
        insta_clock_string = insta_clock_time_list[0]
        insta_clock_string_sliced_int = int(insta_clock_string[6:])
        msg = f"Timer found, waiting {insta_clock_string_sliced_int} seconds..."
        print(msg)
        time.sleep(insta_clock_string_sliced_int + 1)
        driver.find_element_by_id('formcartbutton').click()
        wait()
        try:
            driver.find_element_by_class_name('addcartbutton').click()
            time.sleep(5)
            try:
                congrats_msg = driver.find_element_by_xpath('//*[@id="pricing_table3"]/div/div/div/div/span/center/span')
                success = True
            except:
                success = False
        except:
            pass
    except:
        time.sleep(1)
        try:
            driver.find_element_by_class_name('addcartbutton').click()
            time.sleep(5)
            try:
                congrats_msg = driver.find_element_by_xpath('//*[@id="pricing_table3"]/div/div/div/div/span/center/span/span')
                success = True
            except:
                success = False
        except:
            pass
    if success == True:
        print("Successful! Followers should arrive shortly! Exiting...")
        time.sleep(5)
        driver.quit()
        sys.exit()
    else:
        if(retry <= 9):
            attempt += 1
            msg2 = f"Retrying...{attempt}/10"
            print(msg2)
        retry += 1
print("Unsuccessful! Please try again later.")
time.sleep(5)
driver.quit()
sys.exit()