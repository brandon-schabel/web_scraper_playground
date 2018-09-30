from selenium import webdriver
import time
import cognitive_face as CF
from db_secrets import *
import datetime 

from get_profile_info import *
from buttons_key_presses import *
from login import *
from schemas import Profile
from secrets import login_user, fb_pass, subscription_key

from selenium_playground import *


driver = webdriver.Chrome()

CF.Key.set(subscription_key)

BASE_URL = 'https://westus.api.cognitive.microsoft.com/face/v1.0'
CF.BaseUrl.set(BASE_URL)


load_site(driver)
t_login_fb(driver)