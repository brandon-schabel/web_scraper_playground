import sys
sys.path.append( '../')
import random

from mongoengine import *
from db_secrets import *

from schemas import Profile
from search_for_profile_description import filter_string, find_profiles_with_word

connect('t_database', port=port, host=host, username=user, password=password )

def get_all_words(profiles, filtered=True):  
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
  words_count = {}

  for word in array:
    if(word in words_count):
      words_count[word] += 1
    else:
      words_count[word] = 1
  
  return words_count

# this just flattens to object to the word and numbers for ex.: {"word": 10}
def no_extra(words):
  new_sorted = []
  for each in words:
    new_sorted.append({each["word"]: each["occurs"]})

  return new_sorted

# should be object
def sort_words_by_max(words):
  '''
  pass in object of words in format of
  [{"sample": 10}]
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
  return words[random.randint(0, len(words) - 1)]

def get_rand_unfiltered():
 return get_rand_word(sorted_words_unfiltered)

def get_rand_filtered():
  return get_rand_word(sorted_words_filtered)

def get_rand_sentence(words, length):
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
