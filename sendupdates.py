from __future__ import print_function
from __future__ import unicode_literals
from collections import defaultdict,Counter
 
import fitbit
from datetime import datetime,timedelta
from keys import dane_key
from fbdb import FbData
import sys

# Import the email modules we'll need
from email.mime.text import MIMEText
# Import smtplib for the actual sending function
import smtplib

def send_email(message_text):
	message = message_text

	msg = MIMEText('')
	msg['Subject'] = message
	msg['From'] = 'dane@awr.com'
	msg['To'] = '4086790481@txt.att.net'

	# Send the message via our own SMTP server, but don't include the
	# envelope header.
	s = smtplib.SMTP('us-cam-mail-queue')
	s.sendmail("dane@awr.com", ['4086790481@txt.att.net'], msg.as_string())
	s.quit()


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


d = datetime.now()

s = activity_on_day(authd_client,d)
steps = int(s['steps'])

text = False
if steps < 12000:
	text = 'You need to pick it up, you are only at {} steps'.format(steps)
else:
	x = steps % 5000
	if x > 4750:
		text = 'You are only {} steps away from a breakpoint'.format(5000-x)

if text:
	send_email(text)


authd_client.sleep()


