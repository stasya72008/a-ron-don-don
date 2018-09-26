from selenium import webdriver

from constants import *
from database import *

# prepare_db()

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
        phone_number = driver.find_elements_by_css_selector(PHONE_NUMBER_CSS)[1].text

        if is_not_phone_exists(phone_number):
            profile_link = driver.find_elements_by_css_selector(USER_NAME_CSS)[0].get_attribute('href')
            user_name = driver.find_elements_by_css_selector(USER_NAME_CSS)[0].text.strip()
            price = driver.find_element_by_css_selector('.price-label strong').text
            info_line = driver.find_element_by_class_name(USER_SINCE_CLASS).text

            insert_into_table(phone_number, user_name, link, price, profile_link, info_line)

            print link
            print profile_link
            print phone_number
            print user_name
            print price
            print info_line

driver.close()
