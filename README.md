Fitbit Data Collection and Analysis
===================================

### Overview

While the Fitbit site does provide some basis charting capabilities there
are no analytics available and no way to build your on on that site so
the purpose of this package are to download all the data and then perform
some analytics on the data

This package is based on python-fitbit (https://github.com/orcasgit/python-fitbit)
which does all the heavy lifting.  The purpose of this package is to add:
* a simple local cache of the fitbit data
* a rate limiting download capability to build the local cache
* simple routine to convert the data to a .csv so it can be analyzed.

The local database can support multiple users but this needs more work. 
Currently most things force you to specify which user you want rather than
handling all users at once.  This is a work-in-progress.

### Requirements
* fitbit package: install with pip install fitbit
  this may only run in python 2.7, not sure.

* to get your fitbit keys you need to run gather-keys which you get from
  https://github.com/orcasgit/python-fitbit
  keys.py explains how to set the keys as environment variables




### Scripts in this Package

Due to the API rate limiting you can't just download all of the data. In 
addition, the data will have gaps and errors in it so there needs to be a
way to slowly gather all of the data and then clean and assemble it together.

* download.py
  * usage: donwload.pl user start end
  * download days from start to end (inclusive)
  * start and end are in yyyy-mm-dd format
  * user is one of the users for which keys have been configured
  * will rate limit, if you ask for more than 60 days it will only ask for
    one day per minute to prevent triggering fitbit's rate limit.  It goes 
    slow but lets you download data for an unlimited range of dates.

* db2csv.py
  * usage: db2csv.pl filename.csv
  * converts the database to a csv file named filename.csv

* dbfix.py
  * deletes days that have 0 steps (missing days)

* db.json
  * the database file
  * included database is to use as an example, you should delete this
    before downloading your own data

* fbdb.py
  * interface to the database

* days.py <user>
  * lists the range of dates for which there is data in the database

### Analysis

Currently all the analysis is performed in R. This needs to be moved to an
iPython notebook.

* average and median steps, steps/week, steps/month
* which is better metric, average or median?
* how average/median moves during the year
* correlation of weight to activity
  * correlate weight to activity1-3, sendentary and totals

### Examples

##### Setup
You need to setup your Fitbit keys by setting the environment variables.  See keys.py for instructions on the variables to set. You can set this up to work for multiple users at once.

You should delete db.json so you can setup your own.

##### Loading up the database

```
~/src/fitbit> python download.py dane 2015-03-01 2015-03-05
got data for 2015-03-01
got data for 2015-03-02
got data for 2015-03-03
got data for 2015-03-04
got data for 2015-03-05
```

##### Checking range of data available

```
~/src/fitbit> python days.py dane
Start = 2012-11-01
End   = 2015-03-31
```

##### Generating a CSV file

```
~/src/fitbit> python db2csv.py dane Q1.csv 2015-01-01 2015-03-31
~/src/fitbit> head -n 5 Q1.csv
distance,steps,weight,active1,active2,active3,sedentary,calories,actcal,biking,date,month,year,user
8.52,17393,158,61,65,110,1204,2691,1375,0.0,2015-01-01,1,2015,dane
9.44,19283,158.2,68,131,88,1153,2802,1546,0.0,2015-01-02,1,2015,dane
8.68,17724,157.6,63,53,122,1202,2706,1401,0.0,2015-01-03,1,2015,dane
9.31,19018,157.6,103,133,98,1106,2848,1639,0.0,2015-01-04,1,2015,dane
```


### Requirements

* Python 2.6+
* fitbit
