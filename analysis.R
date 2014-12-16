fb <- read.csv('data.csv')
head(fb)


library(ggplot2)
## simple scatter plot of calories vs steps
### after marking which device the data comes from
fb$dt <- as.Date(fb$date,format="%Y-%m-%d")
fb$device[fb$dt < "2013-08-01"] <- "nike"
fb$device[fb$dt > "2013-07-31"] <- "fitbit"
ggplot(fb,aes(x=steps,y=calories,color=device)) + geom_point()

## simple scatter plot of distance vs steps with regression line
ggplot(fb,aes(x=distance,y=steps)) + geom_point() + 
  stat_smooth(method = "lm", formula = y ~ x, size = 1)
#### how to compute compute RMS error?

## scatter of distance vs calories
ggplot(fb,aes(x=distance,y=calories)) + geom_point()

fb34 = subset(fb,year==2013 | year==2014)

## dual histograms for 2013 and 2014
ggplot(fb34,aes(x=steps,fill=as.factor(year))) + geom_histogram() 

## Add a column that combines month and year so we can plot vs it
fb$ym = fb$year + fb$month/100

## create sum,median and mean per month
library(plyr)
fb_bymonth = ddply(fb,~ym,summarize,sum=sum(steps),mean=mean(steps),median=median(steps))
## remove imcomplete month
fb_bymonth = subset(fb_bymonth,ym != '2014.12')

## line plot of sum and median by month
#### don't want interpolation so convert ym to a factor
fb_bymonth$ym = factor(fb_bymonth$ym)

#### to plot both median and mean together we need to reshape the data
library(reshape2)
x<-melt(fb_bymonth,id=c("ym","sum"),variable.name="name",value.name="value")
ggplot(x,aes(x=ym,y=value,color=name,group=name)) + geom_line()

## plot medians by month with the loess line
ggplot(fb_bymonth,aes(x=ym,y=median,group=1)) + geom_line() + geom_smooth(method = "loess", size = 1.5)

## plot the mean vs month of the year with each year as a separate color
fb_month = ddply(subset(fb,year!=2012),.(month,year),summarize,sum=sum(steps),mean=mean(steps),median=median(steps))
fb_month$year = factor(fb_month$year)
fb_month$month = factor(fb_month$month)
ggplot(fb_month,aes(x=month,y=median,color=year,group=year)) + geom_line()

ggplot(fb,aes(x=as.factor(year),y=steps)) + geom_boxplot()

ggplot(y2013,aes(x=as.factor(month),y=steps)) + geom_boxplot()

