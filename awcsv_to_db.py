""" Take the data generated from parsing the XML file and add it to the database
"""
import fbcache


cache = fbcache.FitbitCache('dane')
cache.read()

m = {
    'steps_per_day': 'steps_aw',
    'cycling': 'cycling_aw',
    'distance': 'distance_aw',
    'flights': 'floors_aw',
    'calories': 'calories_aw'
}

with open('daily_data.csv') as fp:
    for line in fp.readlines():
        line = line.strip()
        day, k, v = line.split(',')
        cache.add_item(day, m[k], round(float(v), 2))

cache.write()
