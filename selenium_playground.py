from selenium import webdriver
import time
driver = webdriver.Chrome()
from secrets import login_user, fb_pass, subscription_key
import cognitive_face as CF
import re
from mongoengine import *
from schemas import Profile
from db_secrets import *
import datetime

connect('t_database', port=port, host=host, username=user, password=password )
#user = Profile(name=, age=, image_url=, occupation=, distance= )
#user.save()

KEY = '90138c83bd2948c7a69a16dc47cf9fbe'
CF.Key.set(KEY)

BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)


def load_site():
  driver.get('https://tinder.com')
  time.sleep(5)

def t_login_phone():
  driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[2]/div/div[3]/div[2]/button').click()
  time.sleep(2)
  phone = driver.find_element_by_xpath('html/body/div[2]/div/div/div[2]/div[2]/div/input')
  phone.send_keys('9514520917')
  driver.find_element_by_xpath('html/body/div[2]/div/div/div[2]/button').click()
  time.sleep(30)
  
def t_login_fb():
  parent_h = driver.current_window_handle
  driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[2]/div/div[3]/div[1]/button').click()
  time.sleep(2)
  handles = driver.window_handles # before the pop-up window closes
  driver.switch_to_window(handles.pop())
  
  driver.find_element_by_xpath('//*[@id="email"]').send_keys(login_user)
  driver.find_element_by_xpath('//*[@id="pass"]').send_keys(fb_pass)
  driver.find_element_by_xpath('//*[@id="u_0_0"]').click()
  driver.switch_to_window(parent_h)

def close_initial_dialogs():
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

def start_swiping():
  like_counter = 0
  no_counter = 0

  time.sleep(5)
  while(True):
    time.sleep(1)
    profile_name_age = get_name_age()
    view_profile()
    time.sleep(1)
    profile_info = get_profile_info()

    print(profile_name_age)
    print(profile_info)

    #print(check_if_multiple_photos())

    if(check_if_multiple_photos()):
      close_profile()
      time.sleep(1)
      image_div = driver.find_element_by_xpath('//*[@id="content"]/div/span/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/span/div')

      profile_image_url = extract_photo_url(image_div)

      image_analysis_result = detect_face(profile_image_url)
      # if no images are found
      if(image_analysis_result == False):
        view_profile()
        next_photo()
        second_image = driver.find_element_by_xpath('//*[@id="content"]/div/span/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[1]/a[2]/div/div[1]/div/div[2]/div/div')

        profile_image_url = extract_photo_url(second_image)

        image_analysis_result = detect_face(profile_image_url)

      time.sleep(2)

      if(image_analysis_result == True):
        user = Profile(name=profile_name_age["name"], age=profile_name_age["age"], image_url=profile_image_url, occupation=profile_info["occupation"], distance=profile_info["distance"], school=profile_info["school"], liked=True, reason="passed", datetime=datetime.datetime.utcnow)
        user.save()

        like()
        like_counter += 1
        print("likes: " + str(like_counter))

      else: 
        user = Profile(name=profile_name_age["name"], age=profile_name_age["age"], image_url=profile_image_url, occupation=profile_info["occupation"], distance=profile_info["distance"], school=profile_info["school"], liked=False, reason="failed image analysis", datetime=datetime.datetime.utcnow)
        print("Nope reason: Failed Image Analysis")
        nope()
        no_counter += 1
        print("Nopes: " + str(no_counter))
    else:
      user = Profile(name=profile_name_age["name"], age=profile_name_age["age"], image_url=profile_image_url, occupation=profile_info["occupation"], distance=profile_info["distance"], school=profile_info["school"], liked=False, reason="one profile image", datetime=datetime.datetime.utcnow)
      "Nope reason: 1 Profile Image"
      nope()

def detect_face(img_url):
  faces = CF.face.detect(img_url, attributes='age,gender')
  #print('faces found' + len(faces))

  if len(faces) == 0:
    # if no face found, try going to second picture
    return False
  else:
    for each in faces:
      print(each)
      attributes = each['faceAttributes']
      if attributes['gender'] == 'female':
        return True
      else:
        return False

def get_name_age():
  name = "None"
  age = 0

  try: 
    name = driver.find_element_by_xpath('//*[@id="content"]/div/span/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[5]/div[1]/div/span[1]').text
  except:
    print("No name found - Exception")
  
  try:
    age = driver.find_element_by_xpath('//*[@id="content"]/div/span/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[5]/div[1]/div/span[2]').text
  except:
    print("No age found - Exception")

  if(age != 0): 
    try:
      age = re.findall(r'\d+', age)
      age = int(age[0])
    except:
      print("Exception: Failed to find age")
      age = 0

  return {
    "name": name,
    "age": age
  }

def get_profile_info():
  occupation = "None"
  school = "None"
  distance = 0

  try: 
    occupation = driver.find_element_by_xpath('//*[@id="content"]/div/span/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div').text
  except:
    print("No occupation found - Exception")
  
  try:
    school = driver.find_element_by_xpath('//*[@id="content"]/div/span/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/div').text
  except:
    print("No school found - Exception")
  
  try:
    distance = driver.find_element_by_xpath('//*[@id="content"]/div/span/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[4]/div/span').text
  except:
    print("No distance found - Exception")
  

  if(distance != 0):
    try: 
      distance = re.findall(r'\d+', distance)
      distance = int(distance[0])
    except:
      print("Failed to find distance")
      distance = 0
  
  return {
    "occupation": occupation,
    "school": school,
    "distance": distance
  }

def like():
  # driver.find_element_by_xpath("//button[@aria-label='Like']").click()
  body = driver.find_element_by_xpath('//*[@id="Tinder"]/body')
  body.send_keys(u'\ue014')

def nope():
  #driver.find_element_by_xpath('//*[@id="content"]/div/span/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/button[2]').click()
  body = driver.find_element_by_xpath('//*[@id="Tinder"]/body')
  body.send_keys(u'\ue012')

def view_profile():
  body = driver.find_element_by_xpath('//*[@id="Tinder"]/body')
  body.send_keys(u'\ue013')

def next_photo():
  body = driver.find_element_by_xpath('//*[@id="Tinder"]/body')
  body.send_keys(u'\ue00d')

def super_like():
  body = driver.find_element_by_xpath('//*[@id="Tinder"]/body')
  body.send_keys(u'\ue007')

def close_profile():
  body = driver.find_element_by_xpath('//*[@id="Tinder"]/body')
  body.send_keys(u'\ue015')

def check_if_multiple_photos():
  try:
    #check to see if second photo element exist
    if(driver.find_element_by_xpath('//*[@id="content"]/div/span/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[1]/a[2]/div/div[1]/div/div[2]')):
      return True
    else: 
      return False
  except:
    "failed at check multiple photos"

def extract_photo_url(photo_string):
  extracted_url = photo_string.value_of_css_property("background-image")
  extracted_url = str(extracted_url).split('"')
  return extracted_url[1]


load_site()
t_login_fb()
close_initial_dialogs()
start_swiping()
