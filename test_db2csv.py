import unittest
import os
import subprocess
from tempfile import mkstemp
import datetime

from fbcache import FitbitCache


# test data
test_data = [
    {'distance': 7.74, 'margcal': 0, 'steps': 15798, 'active3': 0, 'weight': 184.5, 'active1': 540, 'sedentary': 900,
     'calories': 2322, 'actcal': 1269, 'active2': 0},
    {'distance': 4.72, 'margcal': 0, 'steps': 9642, 'active3': 0, 'weight': 184.2, 'active1': 0, 'sedentary': 1440,
     'calories': 2015, 'actcal': 0, 'active2': 0},
    {'distance': 4.92, 'margcal': 0, 'steps': 10049, 'active3': 0, 'weight': 184.2, 'active1': 0, 'sedentary': 1440,
     'calories': 1977, 'actcal': 0, 'active2': 0},
    {'distance': 6.92, 'margcal': 0, 'steps': 14136, 'active3': 0, 'weight': 183.9, 'active1': 670, 'sedentary': 770,
     'calories': 2125, 'actcal': 1225, 'active2': 0}
]


def create_test_user():
    """ write a few days to a test_user.json file """
    fb = FitbitCache('test_user')
    date = datetime.date(2017, 1, 1)
    days_added = 0
    items_added = 0
    for td in test_data:
        days_added += 1
        for k, v in td.items():
            fb.add_item(date, k, v)
            items_added += 1
        date += datetime.timedelta(days=1)
    fb.write()

    return 'test_user'


USER = create_test_user()


def run(args):
    command = ['python', 'db2csv.py'] + args
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    code = p.returncode
    return code, out.decode('utf-8'), err.decode('utf-8')


class TestFitbitDb2Csv(unittest.TestCase):
    def test_usage_message(self):
        """ run without arguments, should get usage message """
        arguments = []
        code, out, err = run(arguments)
        self.assertNotEqual(code, 0)
        self.assertTrue('Usage' in out)
        self.assertTrue('user_name' in out)

    def test_output_stdout(self):
        arguments = [USER]
        code, out, err = run(arguments)
        self.assertEqual(code, 0)
        lines = out.split('\n')
        # first line is the 'Read 4 days message'
        header = lines[1]
        values = lines[2]
        self.assertTrue('date' in header)
        self.assertTrue('steps' in header)
        self.assertTrue('distance' in header)
        self.assertTrue('15798' in values)

    def test_output_to_file(self):
        fn = mkstemp(suffix='.csv', dir='.', text=True)[1]
        arguments = ['-o', fn, USER]
        code, out, err = run(arguments)
        with open(fn) as fp:
            lines = fp.readlines()
        header = lines[0]
        values = lines[1]
        self.assertTrue('date' in header)
        self.assertTrue('steps' in header)
        self.assertTrue('distance' in header)
        self.assertTrue('15798' in values)
        os.remove(fn)


if __name__ == '__main__':
    unittest.main()
