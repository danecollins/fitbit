from __future__ import print_function
from __future__ import unicode_literals
from collections import defaultdict,Counter
 
import fitbit
from datetime import datetime,timedelta
from keys import dane_key
from fbdb import FbData
import sys


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


(consumer_key, consumer_secret, oa) = dane_key()
authd_client = fitbit.Fitbit(consumer_key, consumer_secret, resource_owner_key=oa['oauth_token'], resource_owner_secret=oa['oauth_token_secret'])


oneday = timedelta(1)
d = datetime.strptime(sys.argv[1],'%Y-%m-%d')
fdb = FbData()
fdb.read()

for i in range(0,70):
	s = activity_on_day(authd_client,d)
	w = weight_on_day(authd_client,d)
	s['weight'] = w
	day = d.strftime('%Y-%m-%d')
	print('getting data for {}'.format(day))
	fdb.add_day(day,s)
	d = d + oneday

fdb.write()
authd_client.sleep()
