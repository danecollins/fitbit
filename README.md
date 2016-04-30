Fitbit Data Collection and Analysis
===================================

### Overview

While the Fitbit site does provide some basis charting capabilities there
are no analytics available and no way to build your on on that site so
the purpose of this package are to download all the data and then perform
some analytics on the data

This package is based on python-fitbit (https://github.com/orcasgit/python-fitbit)
The purpose of this package is to add:
* a simple local cache of the fitbit data which can be added to incrementally
* a rate limiting download capability to build the local cache
* simple routine to convert the data to a .csv so it can be analyzed.
* some scripts to allow integration of other exercise or weather data

The local database can support multiple users but this needs more work. 
Currently most things force you to specify which user you want rather than
handling all users at once.  This is a work-in-progress.

### Requirements
* requirements.txt contains all the requirements

With the change to oauth2, getting your keys is now a little more challenging.

To get your fitbit keys:
  1. install all the requirements (pip -r requirements.txt)
  2. Go to dev.fitbit.com and create an app
     * Set 'Application Website' to: http://localhost:8080/
     * Set 'OAuth 2.0 Application Type' to: Client
     * Set 'Callback URL' to: http://localhost:8080/
     *** note the trailing / on those URL's is VERY IMPORTANT
  4. Set an environment variable named FITBIT\_CLIENT\_ID to the value of 'OAuth 2.0 Client ID'
  5. Set an environment variable named FITBIT\_CLIENT\_SECRET to the value of 'Client Secret'
  6. In your default browser go to http://fitbit.com and log into the account whose data you want to access
  7. Keys are stored in a json file for later use.  run: python get\_keys key\_filename

### Setup

Users are mapped to their key file by a dict at the top of download.py.  You must edit this dict
based on the users you want to have.

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

* db2_csv.py
  * usage: db2csv.pl wide|long filename.csv
  * converts the database to a csv file named filename.csv
  * if 'wide' is specified the file will be a table with date as first column followed by a column 
    for each of the items in the cache.  There will be one row per date.
  * if 'long' is specified the file the file will contain 3 columns: date item\_name and item\_value
    with one row for each item (multiple rows will have same date)

* dbfix.py
  * deletes days that have 0 steps (missing days)

* data/<user>.json
  * the cache file for the user

* fbcache.py
  * interface to the database

* days.py <user>
  * lists the range of dates for which there is data in the database

* db2_feather.py
* usage: db2_feather.py wide|long filename
* create a feather file - https://blog.rstudio.org/2016/03/29/feather/
  which is compatible with both R and Pandas dataframes

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
