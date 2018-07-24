
SHELL := /bin/bash

SOURCES = csvtup.py fbcache.py
UTILS = db2csv.py db2long.py dbfix.py get_keys.py days.py download.py
TESTS = test_db2csv.py test_fbcache.py

flake:
	flake8 $(SOURCES) $(UTILS) $(TESTS)

test: flake
	pytest

update_tested_branch: test
	@echo "Checking git status..."
	@git_status=`git status -s | grep -v '^??'`; \
	if [ "$$git_status" != "" ]; then \
		echo "Git not up to date"; \
		echo "------------------------"; \
		echo "$$git_status"; \
		echo "------------------------"; \
		echo "Exiting."; \
		exit 1; \
	fi;
	@echo "Checking github status..."
	git_branch_status=`git status -sb origin master`; \
	if [ "$$git_branch_status" != "## master...origin/master" ]; then \
		echo "origin/master is not up to date"; \
		echo "------------------------"; \
	    echo "$$git_branch_status"; \
		echo "------------------------"; \
		echo "Exiting."; \
		exit 1; \
	fi;
	git fetch origin tested
	git co tested
	git merge master
	git push
	git co master

.fake: update_tested_branch test flake
