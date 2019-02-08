import re
import pdb

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

c = 0

fout = open('apple_data.txt', 'w')
print('[', file=fout)

with open('/Users/dane/data/p/fitness/apple_health_export_2018-12-03/export.xml') as fp:
    for line in fp.readlines():
        c += 1

        line = line.strip()
        d = None

        if hr_pat.match(line):
            m = hr_pat.match(line)
            d = dict(type='hr', source=m.group(1), start=m.group(2), value=m.group(3))
        elif rhr_pat.match(line):
            m = rhr_pat.match(line)
            d = dict(type='restinghr', source=m.group(1), start=m.group(2), end=m.group(3), value=m.group(4))
        elif st_pat.match(line):
            m = st_pat.match(line)
            d = dict(type='step', source=m.group(1), start=m.group(2), end=m.group(3), value=m.group(4))
        elif fc_pat.match(line):
            m = fc_pat.match(line)
            d = dict(type='flights', source=m.group(1), start=m.group(2), end=m.group(3), value=m.group(4))
        elif dst_pat.match(line):
            m = dst_pat.match(line)
            d = dict(type='distance', source=m.group(1), start=m.group(2), end=m.group(3), value=m.group(4))
        elif cyc_pat.match(line):
            m = cyc_pat.match(line)
            d = dict(type='cycling', source=m.group(1), start=m.group(2), end=m.group(3), value=m.group(4))
        elif cy2_pat.match(line):
            m = cy2_pat.match(line)
            d = dict(type='cycling_workout', duration=m.group(1), source=m.group(3), start=m.group(4), end=m.group(5), value=m.group(2))
        elif cal_pat.match(line):
            m = cal_pat.match(line)
            d = dict(type='calories', source=m.group(1), start=m.group(2), end=m.group(3), value=m.group(4))
        elif sys_pat.match(line):
            m = sys_pat.match(line)
            d = dict(type='systolic', source=m.group(1), start=m.group(2), value=m.group(3))
        elif dia_pat.match(line):
            m = dia_pat.match(line)
            d = dict(type='diastolic', source=m.group(1), start=m.group(2), value=m.group(3))
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
            print('no match:', line[:60])
        if d:
            print(d, file=fout)
            print(',', file=fout)

print(']', file=fout)
fout.close()
print(c)
