"""
This is a scrapper that downloads the 'Reporteria Salud Mental' dashboard data from https://informesdeis.minsal.cl/SASVisualAnalytics/

"""
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from time import sleep


driver = webdriver.Chrome()
driver.get('https://informesdeis.minsal.cl/SASVisualAnalytics/')

# wait and click 'btn-submitguest'
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn-submitguest'))).click()

# wait and click id '__text23'
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'fragment3--navigationTabs-2'))).click()

sleep(120)