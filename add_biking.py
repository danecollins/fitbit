from __future__ import print_function
from __future__ import unicode_literals
from collections import defaultdict,Counter
from csvtup import read_csv
from fbdb import FbData

dist = Counter()



fbd = FbData()
fbd.read()

print("\nDatabase contains %d entries" % len(fbd.daylist()))


rows = read_csv('biking.csv',dialect='excel')
print('Read %d binking entries' % len(rows))

for r in rows:
    d1 = float(r.FX75) if r.FX75 != '' else 0.0
    d2 = float(r.FX77) if r.FX77 != '' else 0.0
    d3 = float(r.Other) if r.Other != '' else 0.0
    d4 = float(r.BB) if r.BB != '' else 0.0
    (month,day,year) = r.day.split('/')
    date = '%d-%02d-%02d' % ( int(year)+2000,int(month),int(day))
    dist[date] = d1 + d2 + d3 + d4
    print('%s - %f' % (date, dist[date]))
    fbd.add_biking(date,dist[date])

fbd.write()
