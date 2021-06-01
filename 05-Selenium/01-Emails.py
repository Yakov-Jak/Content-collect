from pprint import pprint
from pymongo import MongoClient
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time

client = MongoClient('127.0.0.1', 27017)
mails_db = client['mails_db']
mails_col = mails_db.mails_col
mails_col.delete_many({})

chrome_options = Options()
chrome_options.add_argument('start-maximized')
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://mail.ru/')
elem = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.NAME, "login")))
elem.send_keys('study.ai_172@mail.ru')
elem.send_keys(Keys.ENTER)
elem = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.NAME, "password")))
elem.send_keys('NextPassword172!')
elem.send_keys(Keys.ENTER)
old_link = 'x'
m_links = []

while True:
    messages = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//a[contains(@class, 'js-letter-list-item')]")))
    for mes in messages:
        link = mes.get_attribute('href')
        m_links.append(link)
    if old_link == link:
        break
    else:
        old_link = link
        messages[-1].send_keys(Keys.PAGE_DOWN)

pprint(len(set(m_links)))

for mes in m_links:
    driver.get(mes)
    time.sleep(3)
    m_info = {}
    m_info['m_subj'] = driver.find_element_by_xpath("//h2[@class='thread__subject']").text
    m_info['m_from'] = driver.find_element_by_xpath("//div[@class='letter__author']/span").get_attribute('title')
    m_info['m_time'] = driver.find_element_by_xpath("//div[@class='letter__date']").text
    m_info['m_body'] = driver.find_element_by_xpath("//div[@class='letter__body']").text
    pprint(m_info)
    mails_col.insert_one(m_info)

driver.close()
