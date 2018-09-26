from selenium import webdriver

from constants import *
from sql import *

# prepare_db()

# firefox_profile = webdriver.FirefoxProfile()
# firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
# driver = webdriver.Firefox(firefox_profile=firefox_profile)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.maximize_window()


driver.get(URL_PATH)

elem_list = driver.find_elements_by_css_selector(ITEMS_LINKS_CSS)
links_list = []


for element in elem_list:
    link = element.get_attribute('href').split('#')[0]
    links_list.append(link)

for link in links_list:
    driver.get(link)
    # Todo: Add check for visited links

    show_phone_number = driver.find_elements_by_css_selector(SHOW_PHONE_NUMBER_CSS)[1]
    show_phone_number.click()
    phone_number = driver.find_elements_by_css_selector(PHONE_NUMBER_CSS)[1].text

    # Todo: Add check for phone existence in DB

    user = driver.find_elements_by_css_selector(USER_NAME_CSS)[0].text.strip()
    price = driver.find_element_by_css_selector('.price-label strong').text
    line = driver.find_element_by_class_name(USER_SINCE_CLASS).text

    # insert_ad_info(link, phone_number, user, price, line)
    print link
    print phone_number
    print user
    print price
    print line

    driver.back()

driver.close()
