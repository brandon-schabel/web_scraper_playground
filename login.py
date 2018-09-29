#from selenium import webdriver
#driver = webdriver.Chrome()
import time
from secrets import *

def t_login_phone(driver):
  driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[2]/div/div[3]/div[2]/button').click()
  time.sleep(2)
  phone = driver.find_element_by_xpath('html/body/div[2]/div/div/div[2]/div[2]/div/input')
  phone.send_keys(phone)
  driver.find_element_by_xpath('html/body/div[2]/div/div/div[2]/button').click()
  time.sleep(30)
  
def t_login_fb(driver):
  parent_h = driver.current_window_handle
  driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[2]/div/div[3]/div[1]/button').click()
  time.sleep(2)
  handles = driver.window_handles # before the pop-up window closes
  driver.switch_to_window(handles.pop())
  
  driver.find_element_by_xpath('//*[@id="email"]').send_keys(login_user)
  driver.find_element_by_xpath('//*[@id="pass"]').send_keys(fb_pass)
  driver.find_element_by_xpath('//*[@id="u_0_0"]').click()
  driver.switch_to_window(parent_h)