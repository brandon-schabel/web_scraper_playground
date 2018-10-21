import sys
from selenium import webdriver
import time
import cognitive_face as CF
from mongoengine import *
import datetime 

### project specific ####
from get_profile_info import *
from buttons_key_presses import *
from login import *
from schemas import Profile
from secrets import *


#### Profile Tools ####
from profile_tools import *

##### tinder api folder #####
sys.path.append( './t-api')
from tinder_api import get_person, get_auth_token
from fb_auth_token import get_fb_access_token, get_fb_id

driver = webdriver.Chrome()

connect('t_database', port=db_port, host=db_host, username=db_user, password=db_password )

CF.Key.set(subscription_key)
BASE_URL = 'https://westus.api.cognitive.microsoft.com/face/v1.0'
CF.BaseUrl.set(BASE_URL)
FIND_SIMILAR = BASE_URL + ''
counter = {
  'likes': 0,
  'nopes': 0
}

API_KEY = ''

def load_site(driver):
  driver.get('https://tinder.com')
  time.sleep(5)

def start_swiping():
  '''
  infite loop to run program indefinitely
  '''
  time.sleep(5)

  while(True):
    result = eval_profile()

def save_profile(profile):
  '''
  save profile to database
  '''
  if(profile["attributes"] == "none"):
    profile["attributes"] = {}
    profile["attributes"]["result"] = "no attributes"
  
  #print(profile["image_url"])
  #print(profile)
  user = Profile(name = profile["name"], age = profile["age"], image_url=profile["image_url"], liked=profile["liked"], reason=profile["reason"], datetime=datetime.datetime.utcnow, attributes=profile["attributes"], user_id=profile["user_id"], api_data=profile["api_data"])
  user.save()

def try_find_image_url(xpath):
  '''
  tries to find image_url based on an xpath passed in
  '''
  try:
    image = driver.find_element_by_xpath(xpath)
  except:
    image = 'no_image_found'

  if image != 'no_image_found':
    return extract_image_url(image)
  else:
    return 'no_image_found'

def extract_image_url(photo_string):
  '''
  given an xpath to an image, extract the photo url
  '''
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
  '''
  Uses microsoft face api to detect faces and return attributes
  '''
  if(img_url != 'no_url'):
    try:
      faces = CF.face.detect(img_url, attributes='gender,smile,hair')

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
  '''
  Check to see if profile has more than one image, if not probably fake
  '''
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
  '''
  returns user_id from profile image url
  '''
  try:
    url = url.split('/')
    print('userid=' + url[3])
    return url[3]
  except:
    return "invalid_url"

def eval_profile():
  '''
  Main profile analysis function
  '''
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
    user["liked"] = False
    user["reason"] = "No reason"
    user["api_data"] = {"data": "no data found "}

    if(user["attributes"] != "none" and user["attributes"]["gender"] == "female"):
      api_data = get_person(user["user_id"])
      if "results" in api_data:
        user["api_data"] = api_data["results"]
      else:
        user["api_data"] = {"data": "no data found "}
      if "bio" in user["api_data"]:
        bio = filter_string(user["api_data"]["bio"])
        print(bio)
        found_word_match = False
        for each in bio:
          print(each)
          if each in filter_words:
            nope(driver)
            user["liked"] = False
            user["reason"] = "Nope reason, found word in bio: " + each
            print("Nope reason, found word in bio: " + each)
            counter['nopes'] += 1
            found_word_match = True
            break;
          else:
            found_word_match = False;
        
        if(found_word_match == False):
          print("didn't find any filter words")
          like(driver)
          user["liked"] = True
          user["reason"] = "passed"
          counter['likes'] += 1
        
      else:
        print("user has no bio")
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
      user["api_data"] = {"data": "none"}
  else:
    print("Nope reason: 1 Profile Image")
    nope(driver)
    user["liked"] = False
    user["reason"] = "one profile image"
    counter['nopes'] += 1
    user["api_data"] = {"data": "none"}
    return False
    
  
  # print(user)
  print(counter)
  save_profile(user)

def eval_num_profiles(num):
  ''' 
  evaluates a set number of profiles
  '''
  while(num > 0):
    eval_profile()
    print(num)
    num = num - 1
    print(num)

def run():
  load_site(driver)
  t_login_fb(driver)
  get_api_token()
  time.sleep(10)
  close_initial_dialogs(driver)
  start_swiping()

def get_api_token():
  '''
  gets and sets api key on startup
  '''
  fb_auth_token = get_fb_access_token(fb_email, fb_pass)
  fb_user_id = get_fb_id(fb_auth_token)
  API_KEY = get_auth_token(fb_auth_token, fb_user_id)

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