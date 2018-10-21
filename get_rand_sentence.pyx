from profile_tools import get_rand_word

def get_rand_sentence(list words, int length): 
  '''
  creates random setence from list of words passed in as
  [{"sample": 10}, {"another": 2}, {"word": 5}]
  '''

  sentence = []
  return_sentence = []
  cdef dict each
  cdef str word

  while length > 0:
    sentence.append(get_rand_word(words))
    length -= 1
  for each in sentence:
    for word in each:
      return_sentence.append(word)

  return ' '.join(return_sentence)