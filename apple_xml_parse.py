# -*- coding: utf-8 -*-
# Run using python apple_xml_parse.py <path to export.xml>
#
# Once csv files are produced use python awcsv_to_db.py to add the data to dane.json
#


import re
import json
import sys
from collections import Counter, defaultdict


def map_source(s):
    return {
        "Dane’s iPhone": 'Phone',
        'Dane Watch 2': 'Watch',
        "Dane's Apple\xa0Watch": 'Watch',
        'Dane Watch 4': 'Watch',
        'Dane_iP8': 'Phone',
        'Health': 'HealthApp',
        'BP': 'BP',
        'OMRON connect': 'BP'
    }.get(s)


def get_date(s):
    # pull date from string
    return s[:10]


hr_pat = re.compile('<Record type="HKQuantityTypeIdentifierHeartRate".*sourceName="([^"]*)".*startDate="([^"]*)" .*value="([\.\de+-]+)".*>')
rhr_pat = re.compile('<Record type="HKQuantityTypeIdentifierRestingHeartRate".*sourceName="([^"]*)".*startDate="([^"]*)".*endDate="([^"]*)" .*value="([\.\de+-]+)".*>')

st_pat = re.compile('<Record type="HKQuantityTypeIdentifierStepCount".*sourceName="([^"]*)".*startDate="([^"]*)".*endDate="([^"]*)" .*value="([\.\de+-]+)".*>')
dst_pat = re.compile('<Record type="HKQuantityTypeIdentifierDistanceWalkingRunning".*sourceName="([^"]*)".*startDate="([^"]*)".*endDate="([^"]*)" .*value="([\.\de+-]+)".*>')
fc_pat = re.compile('<Record type="HKQuantityTypeIdentifierFlightsClimbed".*sourceName="([^"]*)".*startDate="([^"]*)".*endDate="([^"]*)" .*value="([\.\de+-]+)".*>')
cal_pat = re.compile('<Record type="HKQuantityTypeIdentifierBasalEnergyBurned".*sourceName="([^"]*)".*startDate="([^"]*)".*endDate="([^"]*)" .*value="([\.\de+-]+)".*>')
sys_pat = re.compile('<Record type="HKQuantityTypeIdentifierBloodPressureSystolic".*sourceName="([^"]*)".*startDate="([^"]*)" .*value="([\.\de+-]+)".*>')
dia_pat = re.compile('<Record type="HKQuantityTypeIdentifierBloodPressureDiastolic".*sourceName="([^"]*)".*startDate="([^"]*)" .*value="([\.\de+-]+)".*>')
cyc_pat = re.compile('<Record type="HKQuantityTypeIdentifierDistanceCycling".*sourceName="([^"]*)".*startDate="([^"]*)".*endDate="([^"]*)" .*value="([\.\de+-]+)".*>')
cy2_pat = re.compile('<Workout workoutActivityType="HKWorkoutActivityTypeCycling".*duration="([^"]+).*totalDistance="([^"]+).*sourceName="([^"]*)".*startDate="([^"]*)".*endDate="([^"]*)".*>')

def_pat = re.compile('<Record type="([^"]*)".*')
printed = set(['HKQuantityTypeIdentifierHeight', 'HKQuantityTypeIdentifierBodyMass'])


def read_xml(fn):
    c = 0
    output = []
    o = defaultdict(Counter)
    fout = open('apple_data.txt', 'w')
    fm = open('daily_data.csv', 'w')
    fhr = open('apple_hr_data.csv', 'w')
    with open(fn) as fp:
        for line in fp.readlines():
            c += 1

            line = line.strip()
            d = None

            if hr_pat.match(line):
                m = hr_pat.match(line)
                d = dict(type='hr', source=map_source(m.group(1)), start=m.group(2), value=m.group(3))
                print('{},{},{}'.format(d['source'], d['start'], d['value']), file=fhr)
                d = None
            elif rhr_pat.match(line):
                m = rhr_pat.match(line)
                d = dict(type='restinghr', source=map_source(m.group(1)), start=m.group(2), end=m.group(3), value=m.group(4))
            elif st_pat.match(line):
                m = st_pat.match(line)
                d = dict(type='step', source=map_source(m.group(1)), start=m.group(2), end=m.group(3), value=m.group(4))
                if d['source'] == 'Watch':
                    _dt = get_date(d['start'])
                    o['steps_per_day'][_dt] += float(d['value'])
                d = None
            elif fc_pat.match(line):
                m = fc_pat.match(line)
                d = dict(type='flights', source=map_source(m.group(1)), start=m.group(2), end=m.group(3), value=m.group(4))
                if d['source'] == 'Watch':
                    _dt = get_date(d['start'])
                    o['flights'][_dt] += float(d['value'])
                d = None
            elif dst_pat.match(line):
                m = dst_pat.match(line)
                d = dict(type='distance', source=map_source(m.group(1)), start=m.group(2), end=m.group(3), value=m.group(4))
                if d['source'] == 'Watch':
                    _dt = get_date(d['start'])
                    o['distance'][_dt] += float(d['value'])
                d = None
            elif cyc_pat.match(line):
                m = cyc_pat.match(line)
                d = dict(type='cycling', source=map_source(m.group(1)), start=m.group(2), end=m.group(3), value=m.group(4))
                if d['source'] == 'Watch':
                    _dt = get_date(d['start'])
                    o['cycling'][_dt] += float(d['value'])
                d = None
            elif cy2_pat.match(line):
                m = cy2_pat.match(line)
                d = dict(type='cycling_workout', duration=m.group(1), source=m.group(3), start=m.group(4), value=m.group(2))
            elif cal_pat.match(line):
                m = cal_pat.match(line)
                d = dict(type='calories', source=map_source(m.group(1)), start=m.group(2), end=m.group(3), value=m.group(4))
                if d['source'] == 'Watch':
                    _dt = get_date(d['start'])
                    o['calories'][_dt] += float(d['value'])
                d = None
            elif sys_pat.match(line):
                m = sys_pat.match(line)
                d = dict(type='systolic', source=map_source(m.group(1)), start=m.group(2), value=m.group(3))
            elif dia_pat.match(line):
                m = dia_pat.match(line)
                d = dict(type='diastolic', source=map_source(m.group(1)), start=m.group(2), value=m.group(3))
            elif def_pat.match(line):
                m = def_pat.match(line).group(1)
                if 'HKQuantityTypeIdentifierDistanceWalkingRunning' in line:
                    print(line)
                if m not in printed:
                    print(m)
                    printed.add(m)
            elif line.startswith('<MetadataEntry'):
                pass
            elif line.startswith('<InstantaneousBeatsPerMinute'):
                pass
            elif line.startswith('</Record>'):
                pass
            elif line.startswith('<Correlation ') or line.startswith('</Correlation>'):
                pass
            elif line.startswith('<WorkoutEvent ') or line.startswith('</Workout') or line.startswith('<Workout workoutActivityType'):
                pass
            elif 'HeartRateVariabilityMetadataList>' in line:
                pass
            elif ('<Location' in line) or line.startswith('<WorkoutRoute'):
                pass
            elif '<ActivitySummary' in line:
                pass
            else:
                pass
            if d:
                output.append(d)

    print('writing apple_data.txt json file')
    fout.write(json.dumps(output, indent=4))
    fout.close()
    print('writing daily_data.csv')
    for typ, cntr in o.items():
        for dy, v in cntr.items():
            print("{},{},{}".format(dy, typ, v), file=fm)
    fm.close()
    fhr.close()
    print('writing apple_hr_data.csv')
    return o


if len(sys.argv) != 2:
    print('Usage python apple_xml_parse.py path/apple_health_export/export.xml')
    exit(1)

read_xml(sys.argv[1])
