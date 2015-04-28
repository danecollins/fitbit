
from __future__ import print_function
from __future__ import unicode_literals
from collections import namedtuple
import csv
import sys
import os

if os.environ.get('csvtup_debug', '0') == '1':
    print('CSVTUP: debug enabled')
    debug_port = sys.stdout
else:
    debug_port = False


def dprint(*args):
    global debug_port
    if debug_port:
        print(*args, file=debug_port)


if sys.version_info < (3, 0, 0):
    Old_Version = True
else:
    Old_Version = False

dprint("Old_Version = ", Old_Version)

if Old_Version:
    import codecs

    def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
        # csv.py doesn't do Unicode; encode temporarily as UTF-8:
        csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                                dialect=dialect, **kwargs)
        for row in csv_reader:
            # decode UTF-8 back to Unicode, cell by cell:
            yield [unicode(cell, 'utf-8') for cell in row]

    def utf_8_encoder(unicode_csv_data):
        for line in unicode_csv_data:
            yield line.encode('utf-8')
###################################################################################
#                               General Purpose CSV Reader
#
#  Usage:
#         read_csv(filename) is the simplest case
#  Returns:
#         lines are a list of named tuples
#         can be accessed with line[n].fieldname
#
#  Notes:
#    - blank lines are always ignored
#    - if ignore_after_blanks is true, reading stops at first blank line
#    - limitation: currently column names must be valid identifiers (can't be numbers)
#    - spaces in header names will be replaces with _
#    - if not passed in the return field names are taken from the top of the file
#


def read_csv(filename, encoding='utf-8',
             ignore_after_header=0, ignore_after_blank=True,
             fields=False, header=True, max_rows=False,
             **kwargs):

    lineno = 0
    num_rows = 0

    if Old_Version:
        # in 2.7 a character is a str not a byte. For CSV it must be a byte
        # if you're calling it in 2.7 you would use b"|" or bytes("|") but in
        # 3.0 you can't do that so we always pass it in as "|" and check and
        # convert it in 2.7
        if 'delimiter' in kwargs:
            kwargs['delimiter'] = bytes(kwargs['delimiter'])

        dprint(kwargs)

        fp = codecs.open(filename, 'r', encoding=encoding)
        reader = unicode_csv_reader(fp, **kwargs)
    else:
        fp = open(filename, 'r', encoding=encoding)
        reader = csv.reader(fp, **kwargs)

    # If fields are passed in use them for the header otherwise read from file
    if not fields:
        fields = next(reader)
        lineno += 1
        fields = [x.replace(' ', '_') for x in fields]
        # sometimes the file ends with a tab which parses as an extra field
        # need to remove that one.
        fields = [x for x in fields if len(x) > 0]
        dprint("field names = {}".format(fields))
    else:
        if header:
            next(reader)  # just ignore header
            lineno += 1

    # need to test field names (can't be a number)
    names = []
    for f in fields:
        if f[0].isdigit():
            x = '_' + f
            print('changing field named %s to %s' % (f, x))
            f = x
        names.append(f)

    dprint('Tuple Fields:', names)

    CSVF = namedtuple('CSVF', names)
    number_of_fields = len(fields)
    dprint("number_of_fields={}".format(number_of_fields))

    for i in range(ignore_after_header):
        next(reader)
        lineno += 1

    rows = list()
    dprint('Starting to read data at line {}'.format(lineno))

    for x in reader:
        if max_rows and num_rows == max_rows:
            break
        lineno += 1
        num_rows += 1
        if ignore_after_blank and len(x) == 0:
            break
        if len(x) > 0:
            # only keep as many values as there are in the header
            x = x[0:number_of_fields]
            try:
                rows.append(CSVF._make(x))
            except Exception as e:
                print(e)
                print("vector is: {}".format(x))
                print("line number is {}".format(lineno))

    fp.close()
    dprint('Returning %d rows' % len(rows))
    return(rows)


if __name__ == '__main__':

    import unittest

    class CSVtests(unittest.TestCase):
        def test_basic_csv(self):
            # Most basic reading of csv file, but with some blank lines in it
            rows = read_csv('./csv/booking_goals.csv', ignore_after_blank=False,
                            dialect='excel')
            assert len(rows) == 95
            row0 = rows[0]
            assert row0.Amount == '1200000'
            assert row0.Final == '986539'
            assert row0.Goal == 'AP-JPE-NT'
            assert rows[94].Goal == 'WW-quota'
            assert rows[94].pct_of_goal == '0.902'

        def test_tab_separated(self):
            # Simplest tab-separated file
            rows = read_csv('./csv/file1.tsv', dialect='excel-tab')
            assert len(rows) == 27
            assert rows[0].custid == '10000'
            assert rows[26].a2013 == '53953.57'

        def test_odd_delimiter(self):
            # Using odd delimiter and extra header line
            rows = read_csv('./csv/odd_head_and_foot.txt', ignore_after_header=1,
                            dialect='excel', delimiter="|")
            assert len(rows) == 21
            assert rows[0].custid == '1'
            assert rows[1].custname == 'Inside Contactless'
            assert rows[20].city == 'VA'

        def test_excel_from_sfdc(self):
            # Excel file from SFDC with issues
            rows = read_csv('./csv/excel_from_sfdc.csv', encoding='latin1',
                            dialect='excel')

            assert len(rows) == 18004

        def test_passing_in_names(self):
            names = ['CustID', 'CY2010', 'CY2011', 'CY2012', 'CY2013']
            rows = read_csv('./csv/file1.tsv', fields=names,
                            dialect='excel-tab')
            assert len(rows) == 27
            assert rows[0].CustID == '10000'
            assert rows[26].CY2013 == '53953.57'
    unittest.main()
