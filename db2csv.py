from __future__ import print_function
from __future__ import unicode_literals
from collections import defaultdict,Counter
import sys
 
from fbdb import FbData


if len(sys.argv) != 2:
	print('Usage: python db2csv.py outputfile')
	exit(0)
	
fbd = FbData()
fbd.read()

print("\nDatabase contains %d entries" % len(fbd.daylist()))

with open(sys.argv[1],'w') as fp:
    fbd.write_csv(fp)