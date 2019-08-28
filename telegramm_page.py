from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import getpass
import time


from constants import *


def go_to_telegram():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    username = getpass.getuser()
    # chrome_options.add_argument("--user-data-dir=C://Users/{}/AppData/Local/Google/Chrome/User Data".format(username))

    chrome_options.add_argument("--user-data-dir=C://Users/TEMP.SOFTSERVE.000/AppData/Local/Google/Chrome/User Data")

    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.maximize_window()

    wait = WebDriverWait(driver, 10)

    driver.get(TELEGRAM_URL)
    time.sleep(10)

    return driver, wait


def add_number(_driver, _wait, phone):
    _driver.find_element_by_xpath(MENU).click()
    _wait.until(EC.visibility_of_element_located((By.XPATH, CONTACTS))).click()
    _driver.find_element_by_xpath(NEW_CONTACT).click()

    actions = ActionChains(_driver)
    actions.move_to_element(_driver.find_element_by_xpath(FIRST_NAME))
    actions.click()
    actions.move_to_element(_driver.find_element_by_xpath(PHONE_NUMBER))
    actions.click()
    actions.send_keys(phone + Keys.ENTER)
    actions.perform()
    actions.reset_actions()
