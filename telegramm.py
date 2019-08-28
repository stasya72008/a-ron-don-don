import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from constants import *
from helpers import number_format
from database import get_all, insert_into_table, is_telegram_acount, create_bd_telegram

from telegramm_page import add_number, go_to_telegram

create_bd_telegram()

driver, wait = go_to_telegram()


for _line in get_all():
    for number in [number_format(item) for item in _line[0].split('\n')]:
        if is_telegram_acount(number):
            continue

        print(number + '-' * 40)
        try:

            # Addition of phone number
            add_number(driver, wait, number)

            # Error Verification
            try:
                wait_err = WebDriverWait(driver, 3)
                wait_err.until(EC.visibility_of_element_located((By.XPATH, ERROR_NOT_FOUND)))
                insert_into_table(number, 'Not found', table='telegram')
                driver.find_element_by_tag_name('body').send_keys(Keys.ESCAPE + Keys.ESCAPE + Keys.ESCAPE)
                continue
            except TimeoutException:
                try:
                    wait_err = WebDriverWait(driver, 1)
                    wait_err.until(EC.visibility_of_element_located((By.XPATH, ERROR_TOO_FAST)))
                    print('=' * 20 + 'Too fast' + '=' * 20)
                    time.sleep(140)
                    driver.find_element_by_tag_name('body').send_keys(Keys.ESCAPE + Keys.ESCAPE + Keys.ESCAPE)
                    continue
                except TimeoutException:
                    pass

            # Get name and time of visit
            wait.until(EC.visibility_of_element_located((By.XPATH, PROFILE))).click()
            driver.find_element_by_xpath(ACTION_MORE).click()
            wait.until(EC.visibility_of_element_located((By.XPATH, ACTION_DELETE_CONTACT))).click()

            # Removal Waiting
            try:
                WebDriverWait(driver, 3).until_not(
                    EC.presence_of_element_located((By.XPATH, ACTION_DELETE_CONTACT)))
            except TimeoutException:
                # Reopen profile
                driver.find_element_by_xpath(CLOSE).click()
                wait.until(EC.visibility_of_element_located((By.XPATH, PROFILE))).click()
                time.sleep(1)

            user_name = driver.find_element_by_xpath(PROFILE_NAME).text
            last_seen = driver.find_element_by_xpath(PROFILE_SEEN).text
            user_profile = None
            try:
                user_profile = driver.find_element_by_xpath(PROFILE_DESCRIPTION).text
            except:
                pass  # ignore

            insert_into_table(number, user_name, last_seen, user_profile, table='telegram')
            print(user_name)

            driver.find_element_by_xpath(CLOSE).click()
        except Exception as err:
            print(type(err))
            pass

        driver.find_element_by_tag_name('body').send_keys(Keys.ESCAPE + Keys.ESCAPE + Keys.ESCAPE)

driver.close()
