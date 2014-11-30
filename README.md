Fitbit Data Collection and Analysis
===================================

### Overview

While the Fitbit site does provide some basis charting capabilities there
are no analytics available and no way to build your on on that site so
the purpose of this package are to download all the data and then perform
some analytics on the data

### Data Structure

Due to the API rate limiting you can't just download all of the data. In 
addition, the data will have gaps and errors in it so there needs to be a
way to slowly gather all of the data and then clean and assemble it together.

* download.pl
** usage: donwload.pl yyyy-mm-dd
** download 30 days of data starting on yyyy-mm-dd to the database

* db2csv.pl
** usage: db2csv.pl filename.csv
** converts the database to a csv file named filename.csv

* csv2db
* db.json
** the database to date

### Analysis

* average and median steps, steps/week, steps/month
* which is better metric, average or median?
* how average/median moves during the year
* correlation of weight to activity
** correlate weight to activity1-3, sendentary and totals

