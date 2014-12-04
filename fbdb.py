
from __future__ import print_function
from __future__ import unicode_literals
from collections import defaultdict,Counter

import fitbit
import pprint
import json
import datetime

# database is a dict of dates with the value being a fbday object
class FbData:

	def __init__(self, file = './db.json'):
		self.db = {}
		self.__filename__ = file

	def read(self):
		with open(self.__filename__) as f:
			self.db =  json.loads(f.read())

	def write(self):
		with open(self.__filename__, 'w') as f:
			f.write(json.dumps(self.db, indent=2))

	def get_day(self,day):
		return self.db[day]

	def add_day(self,day,data):
		# want to make sure we never set the data back to the wrong day so
		# store the day in the data and use set_day to make changes (which does
		# does not take a day but uses the stored day)

		# Day Format:
		# {'distance': 6.92, 'margcal': 0, 'steps': 14136, 'active3': 0, 
		#  'weight': 183.9, 'active1': 670, 'sedentary': 770, 'calories': 2125, 
		#  'actcal': 1225, 'active2': 0}
		data['date'] = day
		if day in self.db:
			print('ERROR: day {} is already in the data, use set_day'.format(day))
		else:
			self.db[day] = data

	def set_day(self,data):
		day = data['date']
		if day not in self.db:
			print('ERROR: day {} not in data'.format(day))
		else:
			self.db[day] = data

	def exists(self,date):
		return date in self.db

	def num_days(self):
		return len(self.db)

	def daylist(self):
		return(sorted(self.db.keys()))

	def remove_days_without_steps(self):
		removed = list()
		for day in self.daylist():
			if self.db[day]['steps'] == 0:
				del self.db[day]
				removed.append(day)
		return removed

	def find_missing_days(self):
		day = datetime.datetime(2012,11,1)
		end = datetime.datetime.now()
		oneday = datetime.timedelta(days=1)
		db=self.db
		missing = list()
		while day <= end:
			key = day.strftime('%Y-%m-%d')
			if not key in db:
				missing.append(key)
			day = day + oneday
		return missing

	def create_derived_fields(self):
		for k,data in db.items():
			date = datetime.strptime('%Y-%m-%d',k)
			data['day'] = date # .year, .month, .day .isocalendar()[1]

	def write_csv(self,filename):
		pass





