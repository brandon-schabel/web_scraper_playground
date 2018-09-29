import time

def like(driver):
  # driver.find_element_by_xpath("//button[@aria-label='Like']").click()
  body = driver.find_element_by_xpath('//*[@id="Tinder"]/body')
  body.send_keys(u'\ue014')

def nope(driver):
  #driver.find_element_by_xpath('//*[@id="content"]/div/span/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/button[2]').click()
  body = driver.find_element_by_xpath('//*[@id="Tinder"]/body')
  body.send_keys(u'\ue012')

def view_profile(driver):
  body = driver.find_element_by_xpath('//*[@id="Tinder"]/body')
  body.send_keys(u'\ue013')

def next_photo(driver):
  body = driver.find_element_by_xpath('//*[@id="Tinder"]/body')
  body.send_keys(u'\ue00d')

def super_like(driver):
  body = driver.find_element_by_xpath('//*[@id="Tinder"]/body')
  body.send_keys(u'\ue007')

def close_profile(driver):
  body = driver.find_element_by_xpath('//*[@id="Tinder"]/body')
  body.send_keys(u'\ue015')

def close_initial_dialogs(driver):
  time.sleep(5)  
  # welcome to tinder
  driver.find_element_by_xpath('//*[@id="content"]/div/span/div/div[2]/div/div[1]/div[1]/div/div[3]/button').click()

    #enhanced messaging dialog
  driver.find_element_by_xpath('//*[@id="content"]/div/span/div/div[2]/div/div/main/div/div[3]/button').click()

  # location request
  driver.find_element_by_xpath('//*[@id="content"]/div/span/div/div[2]/div/div/div[1]/div/div[3]/button[1]').click()
  time.sleep(1)

  # notification request
  driver.find_element_by_xpath('//*[@id="content"]/div/span/div/div[2]/div/div/div[1]/div/div[3]/button[2]').click()
  time.sleep(1)