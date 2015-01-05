from __future__ import print_function
from __future__ import unicode_literals
from collections import defaultdict,Counter
 
from fbdb import FbData

fbd = FbData()
fbd.read()
users = fbd.get_user_list()

for user in users:

	fbd.set_user(user)
	print("-------------- User: {} ----------------------".format(user))
	print("\nDatabase contains %d entries" % len(fbd.daylist()))

	empty_days = fbd.remove_days_without_steps()
	print("\nRemoving days with zero steps")
	for x in empty_days:
	    print("    %s" % x)

	### this needs to be changed to handle multiple users
	missing_days = fbd.find_missing_days()
	if len(missing_days) > 0:
	    print("\nThese days are missing from the database")
	    for x in missing_days:
	        print("    %s" % x)
	else:
	    print("\nThere are no missing dates")


print("\nWriting out database")
fbd.write()