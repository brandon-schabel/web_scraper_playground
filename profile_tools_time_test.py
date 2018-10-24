import pyximport
pyximport.install()
import timeit
#from profile_tools import *
from profile_tools_cy import *
#from db_connect import get_profiles


py_setup = '''
from profile_tools import sort_words_by_max, count_all_words, get_all_words
from db_connect import get_profiles

from all_words_list import all_words
'''

cy_setup = '''
from profile_tools_cy import sort_words_by_max, count_all_words, get_all_words
from db_connect import get_profiles

from all_words_list import all_words
'''

py = timeit.timeit('sort_words_by_max(count_all_words(all_words))', setup =py_setup, number = 5)
cy = timeit.timeit('sort_words_by_max(count_all_words(all_words))', setup =cy_setup, number = 5)


print(cy, py)
print('Cython is {}x faster'.format(py/cy))