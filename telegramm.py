import getpass
import time

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from helpers import number_format
from database import get_all, insert_into_telegram, is_telegram_acount, create_bd_telegram

create_bd_telegram()

# ToDo Change user_name_pc
# username = getpass.getuser()
# print(username)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--user-data-dir=C://Users/dkuly/AppData/Local/Google/Chrome/User Data")
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")  # applicable to windows os only
chrome_options.add_argument('--no-sandbox')

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.maximize_window()

wait = WebDriverWait(driver, 10)

lines = get_all()[:]

driver.get('https://web.telegram.org/#/im')
time.sleep(20)

for _line in lines:
    for number in [number_format(item) for item in _line[0].split('\n')]:
        # ToDo check by Id

        if is_telegram_acount(number):
            continue

        try:
            # Addition of phone number
            print('-' * 50)
            print(number)

            driver.find_element_by_xpath('//*[@class="tg_head_btn dropdown-toggle"]').click()
            wait.until(EC.visibility_of_element_located((By.XPATH, '//*[contains(text(),"Contacts")]'))).click()
            driver.find_element_by_xpath('//*[contains(text(),"New contact")]').click()

            actions = ActionChains(driver)
            actions.move_to_element(driver.find_element_by_xpath('//*[contains(text(),"First name")]'))
            actions.click()
            actions.move_to_element(driver.find_element_by_xpath('//*[contains(text(),"Phone number")]'))
            actions.click()
            actions.send_keys(number)
            actions.perform()
            actions.reset_actions()

            driver.find_element_by_xpath('//*[contains(text(),"Save")]').click()

            # Error Verification
            try:
                wait_err = WebDriverWait(driver, 3)
                wait_err.until(EC.visibility_of_element_located((By.XPATH, '//*[contains(text(),"Not found")]')))
                insert_into_telegram(number, 'Not found')
                driver.find_element_by_tag_name('body').send_keys(Keys.ESCAPE + Keys.ESCAPE + Keys.ESCAPE)
                continue
            except TimeoutException:
                try:
                    wait_err = WebDriverWait(driver, 1)
                    wait_err.until(EC.visibility_of_element_located((By.XPATH, '//*[contains(text(),"Too fast")]')))
                    print('=' * 20 + 'Too fast' + '=' * 20)
                    time.sleep(140)
                    driver.find_element_by_tag_name('body').send_keys(Keys.ESCAPE + Keys.ESCAPE + Keys.ESCAPE)
                    continue
                except TimeoutException:
                    pass

            # Get name and time of visit
            wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="tg_head_peer_info"]'))).click()
            driver.find_element_by_xpath('//*[contains(text(),"More...")]').click()
            wait.until(EC.visibility_of_element_located((By.XPATH, '//*[contains(text(),"Delete contact")]'))).click()

            # Removal Waiting
            waiting = False
            for _ in range(2):
                try:
                    driver.find_element_by_xpath('//*[contains(text(),"Delete contact")]')
                except NoSuchElementException:
                    break
                time.sleep(1)
            else:
                waiting = True

            driver.find_element_by_xpath('//*[@class="md_modal_action md_modal_action_close"]').click()

            # Go to Profile
            wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="tg_head_peer_info"]'))).click()
            if waiting:
                time.sleep(1)

            user_name = driver.find_element_by_xpath('//*[@class="peer_modal_profile_name"]').text
            last_seen = driver.find_element_by_xpath('//*[@class="peer_modal_profile_description"]').text
            user_profile = None
            try:
                user_profile = driver.find_element_by_xpath('//*[@class="md_modal_iconed_section_wrap md_modal_iconed_section_number"]').text
            except:
                pass

            insert_into_telegram(number, user_name, seen=last_seen, profile=user_profile)
            print(user_name)

            driver.find_element_by_xpath('//*[@class="md_modal_action md_modal_action_close"]').click()
        except Exception as err:
            print(type(err))
            pass

        driver.find_element_by_tag_name('body').send_keys(Keys.ESCAPE + Keys.ESCAPE + Keys.ESCAPE)

driver.close()
