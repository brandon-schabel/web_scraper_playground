import re
import string
import random

from mongoengine import *
from secrets import *
from schemas import Profile

from db_connect import *

rgx = re.compile('[^' + ''.join(string.printable) + ']')
remove_punctuation = re.compile(r'[^\w\s]')

# returns an array, turn to string by do ' '.join(your_array)
cpdef list filter_string(str string):
  '''
  removes all punctuation, emojis, emoticons, and anything else that 
  doesn't represent a normal character, then returns array of all words
  '''
  cdef list return_list = []
  cdef str word
  string = string.replace("\n", ' ')
  cdef list splitStr = string.split(" ")

  for word in splitStr:
    word = word.lower()
    word = rgx.sub('', word)
    word = remove_punctuation.sub(r'', word)
    return_list.append(word)

  return return_list

cpdef list find_profiles_with_word(profiles, str word):
  '''
  return profile all ids with profiles that contain a certain word
  '''
  cdef list profile_ids = []
  cdef str bio
  cdef list filtered_bio
  
  for profile in profiles:
    try:
      bio = profile["api_data"]["bio"]
      filtered_bio = filter_string(bio)

      if word in bio:
        profile_ids.append(profile["tinder_data"]["results"]["_id"])
    except: 
      continue;
  
  return profile_ids

cpdef list get_all_words(profiles, filtered=True):  
  '''
  grabs all profile bios from data base, then puts every word into a list
  '''
  cdef list all_words = []
  cdef str bio
  cdef str each
  cdef list split_bio = []

  for profile in profiles:
    try:
      bio = profile["api_data"]["bio"]
      if filtered:
        split_bio = filter_string(bio)
      else:
        split_bio = bio.split(" ")
      for each in split_bio:
        all_words.append(each)
    except:
      continue;
  return all_words

cpdef dict count_all_words(list word_list):
  '''
  Creates an object that counts the number of occurances of each word 
  in all profile bios, this does not return a sorted list, it returns an object
  '''
  cdef dict words_count = {}
  cdef str word

  for word in word_list:
    if(word in words_count):
      words_count[word] += 1
    else:
      words_count[word] = 1
  
  return words_count

cpdef list no_extra(list words):
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
  cdef list new_sorted = []
  cdef dict each
  
  for each in words:
    new_sorted.append({each["word"]: each["occurs"]})

  return new_sorted

# should be object
cpdef list sort_words_by_max(dict words):
  '''
  pass in list of words in format of
  [{"sample": 10}, {"another": 2}, {"word": 5}]
  '''
  cdef list sorted_words = []
  cdef str word
  cdef int len_sorted
  cdef int occurs 
  cdef dict word_to_insert
  cdef int i
  cdef str curr_sorted_word
  cdef int curr_sorted_occurance

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

cpdef str get_word_occurance(str word, list words_list):
  '''
  pass in a word to be search in a list of search able words,
  the list format should be [{"sample": 10}, {"another": 2}, {"word": 5}]
  '''
  cdef str each

  for each in words_list:
    try:
      if(each[word]):
        return each[word]
        break;
    except:
      continue;

  return "not_found"


cpdef dict get_rand_word(list words):
  '''
  gets random word from list of words passed in as
  [{"sample": 10}, {"another": 2}, {"word": 5}]
  returns as {"sample": 10}
  '''
  cdef dict word = words[random.randint(0, len(words) - 1)]
  return word

cpdef str get_rand_sentence(list words, int length): 
  '''
  creates random setence from list of words passed in as
  [{"sample": 10}, {"another": 2}, {"word": 5}]
  '''
  cdef str sentence = ''
  cdef dict each
  cdef str word
  cdef dict rand_word

  while length > 0:
    rand_word = get_rand_word(words)

    for word in rand_word:
      sentence += word + ' '
    length -= 1

  return sentence