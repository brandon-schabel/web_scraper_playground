import re

def get_name_age(driver):
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

def get_profile_info(driver):
  occupation_svg = 'https://tinder.com/static/build/c50949339ea708367f1b05ceccc832bd.svg'
  school_svg = 'https://tinder.com/static/build/434b27c139fe936af9b28ba6a220219d.svg'
  location_svg = 'https://tinder.com/static/build/a64e9b4a0b2fb990b973b8c95fb81827.svg'

  occupation = "None"
  school = "None"
  distance = 0

  info_items = 0;
  
  try:
    #if(driver.find_element_by_xpath('//*[@id="content"]/div/span/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/img')):
    src1 = driver.find_element_by_xpath('//*[@id="content"]/div/span/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/img').get_attribute("src")
    print('sr1')
    print(src1 == occupation_svg)
    print(driver.find_element_by_xpath('//*[@id="content"]/div/span/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div/text()').text)
    div_text = driver.find_element_by_xpath('//*[@id="content"]/div/span/div/div[1]/div/div/main/div/div/div[1]/div/div[2]/div[1]/div/div[2]/div').text
    print(div_text)
    if(src1 == occupation_svg):
      occupation = div_text
    if(src1 == school_svg):
      school = div_text
    if(src1 == location_svg):
      location = div_text
    print(src1)

  except: 
    "failed to find some profile content"
  
  try:
    print('src2')
    print("in try")
    #if(driver.find_element_by_xpath('//*[@id="content"]/div/span/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/img')):  
    src2 = driver.find_element_by_xpath('//*[@id="content"]/div/span/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/img').get_attribute("src")
    div_text = driver.find_element_by_xpath('//*[@id="content"]/div/span/div/div[1]/div/div/main/div/div/div[1]/div/div[2]/div[1]/div/div[3]/div').text
    if(src2 == school_svg):
      school = div_text
    if(src2 == location_svg):
      location = div_text

  except:
    "failed to find some profile content"

  try:
    print("in try")
    #if(driver.find_element_by_xpath('//*[@id="content"]/div/span/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[4]/img')):
    src3 = driver.find_element_by_xpath('//*[@id="content"]/div/span/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[4]/img').get_attribute("src")
    print(src3)
    location = driver.find_element_by_xpath('//*[@id="content"]/div/span/div/div[1]/div/div/main/div/div/div[1]/div/div[2]/div[1]/div/div[4]/div').text
    print(src3)
  except:

    "failed to find some profile content"
  '''
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
  '''

  return {
    "occupation": occupation,
    "school": school,
    "distance": distance
  }