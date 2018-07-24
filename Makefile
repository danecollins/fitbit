
SOURCES = csvtup.py fbcache.py
UTILS = db2csv.py db2long.py dbfix.py get_keys.py days.py download.py
TESTS = test_db2csv.py test_fbcache.py

flake:
	flake8 $(SOURCES) $(UTILS) $(TESTS)


test: flake
	pytest
