import re
import string
import random

from mongoengine import *
from secrets import *
from schemas import Profile

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
  '''
  removes all punctuation, emojis, emoticons, and anything else that 
  doesn't represent a normal character.
  '''
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
  '''
  return profile all ids with profiles that contain a certain word
  '''
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

connect('t_database', port=db_port, host=db_host, username=db_user, password=db_password )

def get_all_words(profiles, filtered=True):  
  '''
  grabs all profile bios from data base, then puts every word into a list
  '''
  all_words = []
  for profile in profiles:
    try:
      bio = profile["api_data"]["bio"]
      if filtered:
        bio = filter_string(bio)
      else:
        bio = bio.split(" ")
      for each in bio:
        all_words.append(each)
    except:
      continue;
  return all_words


def count_all_words(array):
  '''
  Creates an object that counts the number of occurances of each word 
  in all profile bios, this  does not return a sorted list
  '''
  words_count = {}

  for word in array:
    if(word in words_count):
      words_count[word] += 1
    else:
      words_count[word] = 1
  
  return words_count

def no_extra(words):
  '''
  flattens to object to the word and numbers for ex.: 
  from 
  {
    "word": "my_word",
    "occurs": 10
  } 

  to 
  {"word": 10}
  '''
  new_sorted = []
  for each in words:
    new_sorted.append({each["word"]: each["occurs"]})

  return new_sorted

# should be object
def sort_words_by_max(words):
  '''
  pass in object of words in format of
  [{"sample": 10}, {"another": 2}, {"word": 5}]
  '''
  sorted_words = []
  
  for word in words:
    len_sorted = len(sorted_words)

    occurs = words[word]
    word_to_insert = {
                        "word": word,
                        "occurs": occurs
                      }

    # if no words exist append at 0 index
    if(len_sorted == 0):
      sorted_words.append(word_to_insert)
    # if current word occurance is bigger than the biggest insert at 0
    elif(occurs >= sorted_words[0]["occurs"]):
      sorted_words.insert(0, word_to_insert) 
    # if current word occurance is as small as smallest insert at the end
    elif(occurs <= sorted_words[len_sorted - 1]["occurs"]):
      sorted_words.append(word_to_insert)
    # else loop through array and find where word fits in
    else:
      # loop through the currently sorted array
      for i in range(len_sorted):
        # next compare our word occurs compared with where we are at in the sorted arr
        curr_sorted_word = sorted_words[i]["word"]
        curr_sorted_occurance = sorted_words[i]["occurs"]

        # if the new word occurs is greater than or equal to where we are at in the sorted arr
        # then we want to insert that word where we are at in the array
        if(occurs >= curr_sorted_occurance):
          sorted_words.insert(i, word_to_insert)
          break;
        else:
          continue;
  
  return no_extra(sorted_words)



def get_word_occurance(word, words_array):
  '''
  pass in a word to be search in a list of search able words,
  the list format should be [{"sample": 10}, {"another": 2}, {"word": 5}]
  '''
  for each in words_array:
    try:
      if(each[word]):
        return each[word]
        break;
    except:
      continue;

  return "not found"

profiles = Profile.objects

words_filtered = get_all_words(profiles)
words_counted = count_all_words(words_filtered)
sorted_words_filtered = sort_words_by_max(words_counted)

print(sorted_words_filtered)
'''
print(words_filtered)
print(get_word_occurance('18', words_filtered))

print(find_profiles_with_word(profiles, 'prius'))
'''

words_unfiltered = get_all_words(profiles, filtered=False)
words_unfiltered_counted = count_all_words(words_unfiltered)
sorted_words_unfiltered = sort_words_by_max(words_unfiltered_counted)


def get_rand_word(words):
  '''
  gets random word from list of words passed in as
  [{"sample": 10}, {"another": 2}, {"word": 5}]
  '''
  return words[random.randint(0, len(words) - 1)]

def get_rand_unfiltered():
 return get_rand_word(sorted_words_unfiltered)

def get_rand_filtered():
  return get_rand_word(sorted_words_filtered)

def get_rand_sentence(words, length): 
  '''
  creates random setence from list of words passed in as
  [{"sample": 10}, {"another": 2}, {"word": 5}]
  '''

  sentence = []
  return_sentence = []

  while length > 0:
    sentence.append(get_rand_word(words))
    length -= 1
  for each in sentence:
    for word in each:
      return_sentence.append(word)

  return ' '.join(return_sentence)

def get_quick_sentence():
  return get_rand_sentence(sorted_words_filtered, 5)
