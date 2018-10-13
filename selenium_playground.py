from selenium import webdriver
import time
import cognitive_face as CF
from mongoengine import *
from db_secrets import *
import datetime 

from get_profile_info import *
from buttons_key_presses import *
from login import *
from schemas import Profile
from secrets import login_user, fb_pass, subscription_key

import sys
sys.path.append( './t-api')
from tinder_api_sms import get_person

driver = webdriver.Chrome()

connect('t_database', port=port, host=host, username=user, password=password )

CF.Key.set(subscription_key)
BASE_URL = 'https://westus.api.cognitive.microsoft.com/face/v1.0'
CF.BaseUrl.set(BASE_URL)
FIND_SIMILAR = BASE_URL + ''
counter = {
  'likes': 0,
  'nopes': 0
}

def load_site(driver):
  driver.get('https://tinder.com')
  time.sleep(5)

def start_swiping():
  time.sleep(5)

  while(True):
    result = eval_profile()

def save_profile(profile):
  if(profile["attributes"] == "none"):
    profile["attributes"] = {}
    profile["attributes"]["result"] = "no attributes"
  
  print(profile["image_url"])

  user = Profile(name = profile["name"], age = profile["age"], image_url=profile["image_url"], liked=profile["liked"], reason=profile["reason"], datetime=datetime.datetime.utcnow, attributes=profile["attributes"], user_id=profile["user_id"])
  user.save()

def try_find_image_url(xpath):
  try:
    image = driver.find_element_by_xpath(xpath)
  except:
    image = 'no_image_found'

  if image != 'no_image_found':
    return extract_image_url(image)
  else:
    return 'no_image_found'

def extract_image_url(photo_string):
  try: 
    extracted_url = photo_string.value_of_css_property("background-image")
    extracted_url = str(extracted_url).split('"')
    if(len(extracted_url) >= 0):
      return extracted_url[1]
    else:
      return 'no_url'
  except:
    return 'no_url'
    print('couldn\'t extract image url')

def detect_face(img_url):
  if(img_url != 'no_url'):
    try:
      faces = CF.face.detect(img_url, attributes='gender,smile,hair')
      try:
        print(faces[0]["faceId"])
        print(faces)
      except:
        print("nope")

      if len(faces) == 0:
        # if no face found, try going to second picture
        return "none"
      else:
          return faces[0]["faceAttributes"]
    except:
      return "none"
  else:
    return "none"

def check_if_multiple_photos():
  try:
    #check to see if second photo element exist
    if(driver.find_element_by_xpath('//*[@id="content"]/div/span/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[1]/a[2]/div/div[1]/div/div[2]')):
      return True
    else: 
      return False
  except:
    "failed at check multiple photos"

def eval_next_photo(user_attributes, photo_num, driver):
  xpath = '//*[@id="content"]/div/span/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[1]/a[2]/div/div[1]/div/div[' + str(photo_num) + ']/div/div'
  '''check to see if last photo failed image analysis'''
  time.sleep(2)
  image_url = try_find_image_url(xpath)
  if(image_url == "no_image_found"):
    return "no_image_found"
  user_attributes = detect_face(image_url)
  time.sleep(2)
  return user_attributes
  
def get_user_id(url):
  #"https://images-ssl.gotinder.com/5a2255cfbc08658f77cbc2dd/640x640_5aae7333-854b-4741-900a-fc6e36a4c6b7.jpg"
  try:
    url = url.split('/')
    print('userid=' + url[3])
    return url[3]
  except:
    return "invalid_url"

def eval_profile():
  user = {}
  user["image_url"] = ''

  time.sleep(1)
  profile_name_age = get_name_age(driver)
  user["name"] = profile_name_age["name"]
  user["age"] = profile_name_age["age"]
  user["image_url"] = try_find_image_url('//*[@id="content"]/div/span/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/span/div')
  user["user_id"] = get_user_id(user["image_url"])
  user["attributes"] = detect_face(user["image_url"])

  view_profile(driver)
  time.sleep(1)

  if(check_if_multiple_photos()):

    # if no faces are found
    #print("attributes before checking if none: " + str(user["attributes"]))

    # when no faces are found in profile image, go through other images
    if(user["attributes"] == "none" ):
      checking_photos = True
      photo_count = 0
      while(checking_photos):
        photo_count += 1
        photo_eval = eval_next_photo(user["attributes"], photo_count, driver)

        if(photo_eval == "none"):
          next_photo(driver)
          continue
        elif(photo_eval == "no_image_found"):
          break
        else: 
          user["attributes"] = photo_eval
          break

    time.sleep(2)
    if(user["attributes"] != "none" and user["attributes"]["gender"] == "female"):
      like(driver)
      user["liked"] = True
      user["reason"] = "passed"
      counter['likes'] += 1
    else: 
      print("Nope reason: Failed Image Analysis")
      nope(driver)
      user["liked"] = False
      user["reason"] = "Failed image analysis"
      counter['nopes'] += 1
  else:
    print("Nope reason: 1 Profile Image")
    nope(driver)
    user["liked"] = False
    user["reason"] = "one profile image"
    return False
    counter['nopes'] += 1
  
  # print(user)
  print(counter)
  save_profile(user)

def eval_num_profiles(num):
  while(num > 0):
    eval_profile()
    print(num)
    num = num - 1
    print(num)

def run():
  load_site(driver)
  t_login_fb(driver)
  time.sleep(10)
  close_initial_dialogs(driver)
  start_swiping()







'''
time.sleep(1)

try:
  face_detected = CF.face.detect(user["image_url"])
  time.sleep(1)
  faceId = face_detected[0]["faceId"]
  find_similar = CF.face.find_similars(faceId, face_list_id="t_face_list")
  time.sleep(1)
  print(find_similar)
except:
  print("find similar failed")
'''
        