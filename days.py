from __future__ import print_function
from __future__ import unicode_literals
from collections import defaultdict,Counter
 
from fbdb import FbData

fbd = FbData()
fbd.read()
days = fbd.daylist()
print('Start = {}'.format(days[0]))
print('End   = {}'.format(days[-1]))

