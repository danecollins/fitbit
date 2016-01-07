#!python
from __future__ import print_function
from __future__ import unicode_literals
from fbdb import FbData
from sys import argv

##################################################################
#
# For a given users this prints out the range of dates for which
# the database has data.
#
# It is useful to run before doing a download to know where to
# start.

if len(argv) != 2:
    print('Usage: python days.py user')
    exit(1)


fbd = FbData()
fbd.read()
fbd.set_user(argv[1])
days = fbd.daylist()
print('Start = {}'.format(days[0]))
print('End   = {}'.format(days[-1]))
