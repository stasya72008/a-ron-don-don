from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from constants import *
from helpers import ElementHasAttribute
from database import create_bd, filter_by_links, insert_into_table, \
    is_not_phone_exists

# firefox_profile = webdriver.FirefoxProfile()
# firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
# driver = webdriver.Firefox(firefox_profile=firefox_profile)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.maximize_window()

all_links_list = []

create_bd()
driver.get(URL_PATH)

pages = driver.find_elements_by_css_selector(PAGE_LINK_CSS)
pages_number = int(pages[-1].text) if pages else 1

# Todo: add try-except blocks
for i in range(1, pages_number + 1):
    driver.get(URL_PATH + '&page={}'.format(i))
    elem_list = driver.find_elements_by_css_selector(ITEMS_LINKS_CSS)
    links_list = list()

    for element in elem_list:
        # Todo (specially for prune) - add check for olx
        link = element.get_attribute('href').split('#')[0]
        links_list.append(link)

    all_links_list += filter_by_links(set(links_list))

for link in all_links_list:
    driver.get(link)

    show_phone_number = driver.find_elements_by_css_selector(SHOW_PHONE_NUMBER_CSS)
    if show_phone_number:
        show_phone_number[1].click()
        if show_phone_number[1].get_attribute('style') != PHONE_NUMBER_VISIBLE:
            WebDriverWait(driver, 20).until(ElementHasAttribute(
                (By.CSS_SELECTOR, SHOW_PHONE_NUMBER_CSS), 'style', PHONE_NUMBER_VISIBLE))
            phone_number = driver.find_elements_by_css_selector(PHONE_NUMBER_CSS)[1].text

        if is_not_phone_exists(phone_number):
            profile_link = driver.find_element_by_css_selector(USER_NAME_CSS).get_attribute('href')
            user_name = driver.find_element_by_css_selector(USER_NAME_CSS).text.strip()
            price = driver.find_element_by_css_selector(PRICE_CSS).text
            info_line = driver.find_element_by_class_name(USER_SINCE_CLASS).text
            user_address = driver.find_element_by_css_selector(USER_ADDRESS_CSS).text

            insert_into_table(phone_number, user_name, link, price, profile_link, info_line,
                              user_address)

driver.close()
