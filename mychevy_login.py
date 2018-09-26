from selenium import webdriver
import time
from secrets import login_user
from secrets import login_password
import re

driver = webdriver.Chrome()

def site_login():
  driver.get('https://my.chevrolet.com/login')
  driver.find_element_by_id('login_username').send_keys(login_user)
  driver.find_element_by_id ('login_password').send_keys(login_password)
  driver.find_element_by_id('Login_Button').click()

def get_odometer():
  time.sleep(3)
  close_survey_dialog()
  return driver.find_element_by_class_name('panel-vehicle-mileage-odometer')

def get_charging_stats():
  time.sleep(3)
  close_survey_dialog()
  driver.find_element_by_xpath('//*[@id="content"]/div/div/div/div[2]/div[2]/div/div[1]/div[4]/div/div[2]/div/div/div/center/button').click()
  time.sleep(60)
  #charge_percentage = driver.find_element_by_class_name('ev-status-left').text
  #charge_percentage = re.findall(r'\d+', charge_percentage)
  #print(charge_percentage)
  # first number is the number of miles, second number is charge percentage
  miles_remaining = driver.find_element_by_class_name('ev-miles-container ').text
  miles_remaining = re.findall(r'\d+', miles_remaining)
  print(miles_remaining)

def close_survey_dialog():
  try:
    if(driver.find_element_by_xpath('//*[@id="IPEinvL126539"]/img')):
      driver.find_element_by_xpath('//*[@id="IPEinvL126539"]/map/area[3]').click()
  except:
    "No survey dialog"
  
def go_to_dashboard():
  driver.find_element_by_xpath('//*[@id="ocnaApp"]/div/div/header/div/div[2]/a/img').click()
  time.sleep(20)

site_login()
time.sleep(5)
get_charging_stats()
go_to_dashboard()
get_charging_stats()
