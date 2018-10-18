import re
import string

emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00010000-\U0010ffff"
                           "]+", flags=re.UNICODE)

rgx = re.compile('[^' + ''.join(string.printable) + ']')
remove_punctuation = re.compile(r'[^\w\s]')

# returns an array, turn to string by do ' '.join(your_array)
def filter_string(string):
  return_array = []
  for word in string.split(" "):
    word = word.lower()
    word = rgx.sub('', word)
    word = emoji_pattern.sub(r'', word)
    word = remove_punctuation.sub(r'', word)
    word = word.split('\n')
    
    for each in word:
      if(len(each) > 0):
        return_array.append(each)
  
  return return_array

def find_profiles_with_word(profiles, word):
  profile_ids = []
  
  for profile in profiles:
    try:
      bio = profile["api_data"]["bio"]
      filtered_bio = filter_string(bio)

      if word in bio:
        profile_ids.append(profile["tinder_data"]["results"]["_id"])
    except: 
      continue;
  
  return profile_ids