import pyximport
pyximport.install()

import timeit

import get_rand_sentence
import profile_tools
words = '''[
  {
    "take" : 22
  },
  {
    "an" : 21
  },
  {
    "no" : 20
  },
  {
    "people" : 20
  },
  {
    "good" : 20
  },
  {
    "this" : 19
  },
  {
    "up" : 19
  },
  {
    "from" : 19
  },
  {
    "want" : 19
  },
  {
    "swipe" : 19
  },
  {
    "music" : 18
  },
  {
    "who" : 18
  },
  {
    "here" : 18
  },
  {
    "what" : 18
  }
]'''

cy = timeit.timeit('get_rand_sentence.get_rand_sentence({},3)'.format(words), setup ='import get_rand_sentence', number = 50000)
py = timeit.timeit('profile_tools.get_rand_sentence({},3)'.format(words), setup ='import profile_tools', number = 50000)

print(cy, py)
print('Cython is {}x faster'.format(py/cy))