from selenium.webdriver.common.keys import Keys

from database import set_user_processed, get_unprocessed_users

from telegramm_page import add_number, go_to_telegram

message = 'http://www.aurum-security.de/'


driver, wait = go_to_telegram()



# for number in get_unprocessed_users():
for number in ['380677703787', '491714478861', '380935384082']:
    try:
        print(number + '-' * 40)

        add_number(driver, wait, number)

        # wait.until(EC.visibility_of_element_located((By.XPATH, TEXT_AREA))).send_keys(message)
        # driver.find_element_by_xpath(BUTTON_SEND).click()

        set_user_processed(number)

    except Exception as err:
        print(type(err))
        pass

    driver.find_element_by_tag_name('body').send_keys(Keys.ESCAPE + Keys.ESCAPE + Keys.ESCAPE)

driver.close()
