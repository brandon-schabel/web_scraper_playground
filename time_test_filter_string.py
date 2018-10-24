import pyximport
pyximport.install()

import timeit

import profile_tools_cy 
import profile_tools


cy = timeit.timeit('profile_tools_cy.filter_string("434 fhdfkdh ejr3h3j r3 r33i4i3 3 r r 3rer fhdksfdskfhdsfh dfdshfjhd")', setup ='import profile_tools_cy', number = 50000)
py = timeit.timeit('profile_tools.filter_string("434 fhdfkdh ejr3h3j r3 r33i4i3 3 r r 3rer fhdksfdskfhdsfh dfdshfjhd")', setup ='import profile_tools', number = 50000)

print(cy, py)
print('Cython is {}x faster'.format(py/cy))