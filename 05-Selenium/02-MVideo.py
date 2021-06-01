from pprint import pprint
from pymongo import MongoClient
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import json

client = MongoClient('127.0.0.1', 27017)
mvideo_db = client['MVideo_db']
mvideo_col = mvideo_db.mvideo_col
mvideo_col.delete_many({})

chrome_options = Options()
chrome_options.add_argument('start-maximized')
# chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.mvideo.ru/?cityId=CityCZ_7173')
ancor = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='header-main__logo']")))
ancor.send_keys(Keys.PAGE_DOWN)
ancor.send_keys(Keys.PAGE_DOWN)
Next_button = WebDriverWait(driver, 10).\
    until(EC.element_to_be_clickable((By.XPATH, "//h2[contains(text(), 'Новинки')]"
                                                "/ancestor::div[contains(@class, 'facelift')]"
                                                "//a[contains(@class, 'next-btn')]")))
it_num = 1
it_num_ = 0
while it_num != it_num_:
    actions = ActionChains(driver)
    actions.move_to_element(Next_button)
    actions.click(Next_button)
    actions.perform()
    time.sleep(1)
    items = driver.find_elements_by_xpath(
        "//h2[contains(text(), 'Новинки')]/ancestor::div[contains(@class, 'facelift')]//li")
    it_num_ = it_num
    it_num = len(items)

for item in items:
    item_info = item.find_element_by_xpath(".//h3/a").get_attribute('data-product-info')
    item_info_json = json.loads(item_info)
    item_info_json['link'] = item.find_element_by_xpath(".//h3/a").get_attribute('href')
    pprint(item_info_json)
    mvideo_col.insert_one(item_info_json)

driver.close()