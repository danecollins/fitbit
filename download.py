from __future__ import print_function
from __future__ import unicode_literals
from collections import defaultdict,Counter
 
import fitbit
from datetime import datetime,timedelta
from keys import dane_fitbit_key
from fbdb import FbData
import sys
import time


def weight_on_day(c, d):
	body = c.body(d)
	try:
		return(body['body']['weight'])
	except:
		print('ERROR in getting weight')
		print(body)

def activity_on_day(c,d):
	act = c.activities(d)
	s = act['summary']
	summary = { 'calories' : s['caloriesOut'],
			'actcal' : s['activityCalories'],
			'margcal' : s['marginalCalories'],
			'distance' : s['distances'][0]['distance'],
			'sedentary' : s['sedentaryMinutes'],
			'active1' : s['lightlyActiveMinutes'],
			'active2' : s['fairlyActiveMinutes'],
			'active3' : s['veryActiveMinutes'],
			'steps' : s['steps'] }
	return(summary)


if len(sys.argv) != 4:
	print('Usage: python download.py dane|cindy startdate enddate')
	exit(0)

(consumer_key, consumer_secret, dane_oa, cindy_oa) = dane_fitbit_key()
if sys.argv[1] == 'dane':
	oa = dane_oa
elif sys.argv[1] == 'cindy':
	oa = cindy_oa
else:
	print( '{} is not a valid user'.format(sys.argv[1]))
	exit(1)


authd_client = fitbit.Fitbit(consumer_key, consumer_secret, resource_owner_key=oa['oauth_token'], resource_owner_secret=oa['oauth_token_secret'])


oneday = timedelta(1)
d = datetime.strptime(sys.argv[2],'%Y-%m-%d')
de = datetime.strptime(sys.argv[3],'%Y-%m-%d')

fdb = FbData()
fdb.read()
fdb.set_user(sys.argv[1])

## get data one day at a time

while d <= de:
	s = activity_on_day(authd_client,d)
	w = weight_on_day(authd_client,d)
	s['weight'] = w
	day = d.strftime('%Y-%m-%d')
	print('getting data for {}'.format(day))
	fdb.add_day(day,s)
	d = d + oneday
	fdb.write()
	time.sleep(60)

authd_client.sleep()
