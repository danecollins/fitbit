"""
This gets data from WeatherUnderground and stores it as data for a user named 'weather'

Currently the goal is to get the highest temperature and humidity for the day but could be change
to keep other metrics.
"""
# compatibility imports
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# standard python includes
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import datetime
import time
import fbcache


def convert_time(s):
    """
    Convert time from am/pm string to floating point - I'm sure this is done in datetime, should convert to that
    :param s: time as string
    :return:  time as float 0-24
    """
    am = s[-2:]
    (h, m) = s[:-3].split(':')
    h = float(h)
    m = float(m)
    if am == 'PM':
        h += 12
    return h + m / 60


def clean_data(d):
    """ Cleans raw wunderground data

    :param d: raw data from wunderground
    :return: lines of data split by newlines and stripped of html syntax
    """
    lines = d.split('\n')
    lines = [l.replace('<br />', '') for l in lines if l]
    return lines


def get_fields(d):
    """ Cleans raw wunderground data

    :param d: cleaned data from wunderground
    :return: list of lists with just the fields of interest
    """
    fields_to_keep = [0, 1, 3, 7, 9, 11]
    header = d[0]
    header_fields = header.split(',')

    # because time goes from PDT to PST replace the header with just time
    header_fields[0] = 'Time'
    result = []
    for line in d[1:]:
        fields = line.split(',')
        r = {}
        for f in fields_to_keep:
            r[header_fields[f]] = fields[f]
        result.append(r)
    return result


def get_keepers(d):
    """ Convert from raw wunderground field list to data we want to use
        Keeps the highest temp, total rain, etc

    :param d: raw data from wunderground
    :return: dict with high_temp, wind, humidity, etc
    """
    first_time = 10
    last_time = 18

    best = dict(high_temp=0, wind=0, cond='', humid=0, rain=0)
    for record in d:
        tm = convert_time(record['Time'])
        if first_time <= tm <= last_time:
            try:
                temp = float(record.get('TemperatureF', 0))
            except ValueError:
                temp = 0
            if temp > best['high_temp']:
                best['high_temp'] = temp
                best['cond'] = record['Conditions']
                try:
                    wind = float(record.get('Wind SpeedMPH', 0))
                except ValueError:
                    wind = 1
                best['wind'] = wind
                try:
                    humid = float(record.get('Humidity', 0))
                except ValueError:
                    humid = 0
                best['humid'] = humid

            try:
                rain = float(record.get('PrecipitationIn', 0))
            except ValueError:
                rain = 0
            if rain > best['rain']:
                best['rain'] = rain
    return best


def get_day(year, month, day):
    """ Retrieves data for one day from wunderground

    This is currently hard coded to the San Jose, CA airport but can be remapped to any wunderground station with
    history.

    :param year: as integer
    :param month: as integer
    :param day: as integer
    :returns dict(high_temp=0, wind=0, cond='', humid=0, rain=0)

    """
    base_url = r'https://www.wunderground.com/history/airport/KSJC/{}/{}/{}/DailyHistory.html?req_city=Campbell&req_state=CA&req_statename=California&reqdb.zip=95008&reqdb.magic=1&reqdb.wmo=99999&format=1'


    url = base_url.format(year, month, day)

    f = urlopen(url)
    data = f.read()
    data = data.decode('utf-8')
    f.close()
    lines = clean_data(data)
    output = get_fields(lines)
    summary = get_keepers(output)
    return summary


def add_days(fbcache, day, stop):
    """
    Add a range of days to the fbcache under the user_name of 'weather'.

    Note: does not write out fbcache object.

    :param fbcache: loaded fbcache object
    :param day: start date as datetime object
    :param stop: end date as datetime object
    :return: number of days added
    """

    days_added = 0
    while day <= stop:
        days_added += 1
        data = get_day(day.year, day.month, day.day)
        for name, value in data.items():
            fbcache.add_item(day, name, value)

        day += datetime.timedelta(days=1)
        time.sleep(1)  # to prevent wunderground from getting upset.  may not be necessary.

    return days_added


if __name__ == "__main__":
    start = datetime.datetime(2014, 3, 8)
    end = datetime.datetime(2016, 1, 1)
    fbcache = fbcache.FitbitCache('weather')
    fbcache.read()
    add_days(fbcache, start, end)
    fbcache.write()