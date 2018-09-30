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

driver = webdriver.Chrome()

connect('t_database', port=port, host=host, username=user, password=password )

CF.Key.set(subscription_key)
BASE_URL = 'https://westus.api.cognitive.microsoft.com/face/v1.0'
CF.BaseUrl.set(BASE_URL)
FIND_SIMILAR = BASE_URL + ''

def load_site(driver):
  driver.get('https://tinder.com')
  time.sleep(5)

def start_swiping():
  user = {}
  counter ={
    'likes': 0,
    'nopes': 0
  }

  time.sleep(5)

  while(True):
    user["image_url"] = ''

    time.sleep(1)
    profile_name_age = get_name_age(driver)
    user["name"] = profile_name_age["name"]
    user["age"] = profile_name_age["age"]
    user["image_url"] = try_find_image_url('//*[@id="content"]/div/span/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/span/div')
    user["attributes"] = detect_face(user["image_url"])

    view_profile(driver)
    time.sleep(1)

    if(check_if_multiple_photos()):
      #close_profile(driver)
      time.sleep(1)

      try:
        face_detected = CF.face.detect(user["image_url"])
        faceId = face_detected[0]["faceId"]
        time.sleep(1)
        find_similar = CF.face.find_similars(faceId, face_list_id="t_face_list")
        time.sleep(1)
        print(find_similar)
      except:
        print("find similar failed")

      # if no faces are found
      print("attributes before checking if none: " + str(user["attributes"]))
      if(user["attributes"] == "none"):
        time.sleep(2)
        #view_profile(driver)
        next_photo(driver)
        second_image_url = try_find_image_url('//*[@id="content"]/div/span/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[1]/a[2]/div/div[1]/div/div[1]/div/div')
        user["attributes"] = detect_face(second_image_url)
        #print("second image attributes: " + str(user["attributes"]))
        time.sleep(2)

        if(user["attributes"] == "none"):
          print("third photo")
          next_photo(driver)
          third_image_url = try_find_image_url('//*[@id="content"]/div/span/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[1]/a[2]/div/div[1]/div/div[3]/div/div')
          user["attributes"] = detect_face(third_image_url)

          time.sleep(2)
          if(user["attributes"] == "none"):
            print("fourth photo")
            next_photo(driver)
            third_image_url = try_find_image_url('//*[@id="content"]/div/span/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[1]/a[2]/div/div[1]/div/div[4]/div/div')
            user["attributes"] = detect_face(third_image_url)
          

      time.sleep(2)
      if(user["attributes"] != "none" and user["attributes"]["gender"] == "female"):
        like(driver)
        counter['likes'] += 1
        user["liked"] = True
        user["reason"] = "passed"
      else: 
        print("Nope reason: Failed Image Analysis")
        nope(driver)
        counter['nopes'] += 1
        user["liked"] = False
        user["reason"] = "Failed image analysis"
    else:
      print("Nope reason: 1 Profile Image")
      nope(driver)
      counter['nopes'] += 1
      user["liked"] = False
      user["reason"] = "one profile image"
    
    print(user)
    save_profile(user)
    print(counter)



def save_profile(profile):
  if(profile["attributes"] == "none"):
    profile["attributes"] = {}
    profile["attributes"]["result"] = "no attributes"
  
  print(profile["image_url"])

  user = Profile(name = profile["name"], age = profile["age"], image_url=profile["image_url"], liked=profile["liked"], reason=profile["reason"], datetime=datetime.datetime.utcnow, attributes=profile["attributes"])
  user.save()

def try_find_image_url(xpath):
  try:
    image = driver.find_element_by_xpath(xpath)
  except:
    image = 'no_image_found'

  if image != 'no_image_found':
    return extract_image_url(image)
  else:
    return 'no_url'

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
    print('couldn\'t extract second image url')

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

### profile info 

load_site(driver)
t_login_fb(driver)
close_initial_dialogs(driver)
start_swiping()