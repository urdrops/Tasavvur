import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument("--disable-extensions")
service = Service(executable_path='/home/kovanskiy/PycharmProjects/TasavvurMain'
                                  '/tasavvur_project/chromedriver-linux64/chromedriver')
driver = webdriver.Chrome(service=service, options=options)
url = 'https://data.egov.uz/rus/spheres/607fea677b6428eee08802b1'

for i in range(10):
    data = driver.find_elements(By.XPATH, "//*[contains(@class, 'd-flex') and contains(@class, 'flex-column') and "
                                          "contains(@class, 'padding-thirty') and contains(@class, 'radius-ten') and "
                                          "contains(@class, 'bg-white')]")[i]
    try:
        link = data.find_element(By.CLASS_NAME, 'page-blue-title')
        time.sleep(2)
        link.click()
        time.sleep(2)
        driver.execute_script("window.history.go(-1)")
        time.sleep(2)
    except Exception as ex:
        print(ex)

