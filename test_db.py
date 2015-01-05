import unittest
import fbdb

class TestParserFunctions(unittest.TestCase):
    def test_dbcreate(self):

        with open('./test.db','w') as fp:
            fp.write('xxx')

        fbd = fbdb.FbData('./test.db')
        fbd.set_user('testuser')
        day1 = {'distance': 7.74, 'margcal': 0, 'steps': 15798, 'active3': 0, 'weight': 184.5, 'active1': 540, 'sedentary': 900, 'calories': 2322, 'actcal': 1269, 'active2': 0}
        day2 = {'distance': 4.72, 'margcal': 0, 'steps': 9642, 'active3': 0, 'weight': 184.2, 'active1': 0, 'sedentary': 1440, 'calories': 2015, 'actcal': 0, 'active2': 0}
        day3 = {'distance': 4.92, 'margcal': 0, 'steps': 10049, 'active3': 0, 'weight': 184.2, 'active1': 0, 'sedentary': 1440, 'calories': 1977, 'actcal': 0, 'active2': 0}
        day4 = {'distance': 6.92, 'margcal': 0, 'steps': 14136, 'active3': 0, 'weight': 183.9, 'active1': 670, 'sedentary': 770, 'calories': 2125, 'actcal': 1225, 'active2': 0}
        fbd.add_day('2014-11-01',day1)
        fbd.add_day('2014-11-02',day2)
        fbd.add_day('2014-11-03',day3)
        fbd.add_day('2014-11-04',day4)
        fbd.write()

        with open('./test.db') as fp:
            lines = fp.readlines()
            self.assertEqual( len(lines), 56)

    def test_dbread(self):
        fbd = fbdb.FbData('./test.db')
        fbd.read()
        fbd.set_user('testuser')
        assert fbd.num_days() == 4

    def test_get_day(self):
        fbd = fbdb.FbData('./test.db')
        fbd.read()
        fbd.set_user('testuser')  
        day = fbd.get_day('2014-11-02')
        assert day['distance'] == 4.72
        assert day['steps']    == 9642
        day = fbd.get_day('2014-11-04')
        assert day['steps']    == 14136

    def test_changing_a_day(self):
        fbd = fbdb.FbData('./test.db')
        fbd.read()
        fbd.set_user('testuser')    
        day = fbd.get_day('2014-11-02')  
        day['steps'] = 20000
        fbd.set_day(day)
        fbd.write()
        newfbd = fbdb.FbData('./test.db')
        newfbd.read()
        fbd.set_user('testuser')  
        assert fbd.get_day('2014-11-02')['steps'] == 20000

    def test_exists(self):
        fbd = fbdb.FbData('./test.db')
        fbd.read()
        fbd.set_user('testuser')  
        assert fbd.exists('2014-11-01')
        assert fbd.exists('2014-11-04')
        assert not fbd.exists('2014-11-05')

if __name__ == '__main__':
    unittest.main()