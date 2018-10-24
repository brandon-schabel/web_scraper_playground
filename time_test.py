import pyximport
pyximport.install()

import timeit

import get_rand_sentence
import profile_tools

cy = timeit.timeit('get_rand_sentence.get_rand_sentence({},3)'.format(words), setup ='import get_rand_sentence', number = 50000)
py = timeit.timeit('profile_tools.get_rand_sentence({},3)'.format(words), setup ='import profile_tools', number = 50000)

print(cy, py)
print('Cython is {}x faster'.format(py/cy))