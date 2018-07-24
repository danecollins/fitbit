import unittest
import datetime
import os
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


def populate_fb_object(obj, day_incr=1):
    date = datetime.date.today()
    days_added = 0
    items_added = 0
    for td in test_data:
        days_added += 1
        for k, v in td.items():
            obj.add_item(date, k, v)
            items_added += 1
        date = date + datetime.timedelta(days=day_incr)
    return days_added, items_added


class TestFitbitCache(unittest.TestCase):

    def test_object_creation(self):
        fb = FitbitCache('test_user')

        self.assertTrue(isinstance(fb, dict))
        self.assertEqual(fb.user_name, 'test_user')

    def test_adding_data(self):
        fb = FitbitCache('test_user')
        date = datetime.date.today()
        i = 0
        for k, v in test_data[0].items():
            fb.add_item(date, k, v)
            i += 1

        self.assertEqual(len(fb), 1)
        self.assertTrue(date in fb)
        self.assertEqual(len(fb[date]), i)

    def test_writing_file(self):
        fb = FitbitCache('test_user')
        if os.path.exists(fb.filename):
            os.remove(fb.filename)
        populate_fb_object(fb)
        fb.write()
        self.assertTrue(os.path.exists(fb.filename))

    def test_reading_file(self):
        fb = FitbitCache('test_user')
        (dates, items) = populate_fb_object(fb)
        fb.write()

        test_object = FitbitCache('test_user')
        test_object.read()
        self.assertEqual(len(test_object), dates)
        i = 0
        for day in test_object:
            for item in test_object[day]:
                i += 1
        self.assertEqual(i, items)

    def test_num_days(self):
        fb = FitbitCache('test_user')
        (dates, items) = populate_fb_object(fb)
        self.assertEqual(fb.num_days(), dates)

    def test_missing_days(self):
        fb = FitbitCache('test_user')
        (dates, items) = populate_fb_object(fb, day_incr=2)
        x = fb.find_missing_days()
        self.assertEqual(len(x), dates - 1)  # given n days with a gap, there are n-1 missing


if __name__ == '__main__':
    unittest.main()
