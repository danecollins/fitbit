from __future__ import print_function
from __future__ import unicode_literals
from collections import Counter
from csvtup import read_csv
from fbdb import FbData

########################################################################
# Reads biking data from a csv file and adds it to the database
#
# CSV file is of the form:
#      date, FX75, FX77, Other, BB
#    mm/dd/yy, mileage for each bike
#
# Note: the total distance is added to the database.  it is not
#       maintained per bike.


def add_biking_data():
    dist = Counter()

    fbd = FbData()
    fbd.read()
    fbd.set_user('dane')

    print("\nDatabase contains %d entries" % len(fbd.daylist()))

    rows = read_csv('biking.csv', dialect='excel')
    print('Read %d binking entries' % len(rows))

    for r in rows:
        fbd.add_biking(r.day, float(r.distance))
        print(r.day, r.distance)
    
    fbd.write()

if __name__ == '__main__':
    add_biking_data()
