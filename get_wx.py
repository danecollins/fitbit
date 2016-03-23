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
import pprint
pp = pprint.PrettyPrinter(indent=4)


def convert_time(s):
    am = s[-2:]
    (h, m) = s[:-3].split(':')
    h = float(h)
    m = float(m)
    if am == 'PM':
        h += 12
    return h + m / 60


def clean_data(d):
    lines = d.split('\n')
    lines = [l.replace('<br />', '') for l in lines if l]
    return lines


def get_fields(d):
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
    first_time = 10
    last_time = 18

    best = dict(high_temp=0, wind=0, cond='', humid=0, rain=0)
    for record in d:
        tm = convert_time(record['Time'])
        if first_time <= tm <= last_time:
            try:
                temp = float(record['TemperatureF'])
            except:
                temp = 0
            if temp > best['high_temp']:
                best['high_temp'] = temp
                best['cond'] = record['Conditions']
                try:
                    wind = float(record['Wind SpeedMPH'])
                except:
                    wind = 1
                best['wind'] = wind
                try:
                    humid = float(record['Humidity'])
                except:
                    humid = 0
                best['humid'] = humid

            try:
                rain = float(record['PrecipitationIn'])
            except:
                rain = 0
            if rain > best['rain']:
                best['rain'] = rain
    return best


def get_day(year, month, day):
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


start = datetime.datetime(2014, 3, 8)
end = datetime.datetime(2016, 1, 1)
day = start

fp = open('weather.csv', 'w')

print('day,temp,humid,rain,wind,cond')
print('day,temp,humid,rain,wind,cond', file=fp)
while day < end:
    data = get_day(day.year, day.month, day.day)
    day_str = day.strftime('%Y-%m-%d')
    data['day'] = day_str
    print('{day},{high_temp},{humid},{rain},{wind},{cond}'.format(**data))
    print('{day},{high_temp},{humid},{rain},{wind},{cond}'.format(**data), file=fp)
    day += datetime.timedelta(days=1)
    time.sleep(1)


