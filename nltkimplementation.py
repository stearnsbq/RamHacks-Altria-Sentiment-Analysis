import nltk
import matplotlib.pyplot as plt
import datetime as dt
from string import punctuation
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.corpus import stopwords 
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.dates as mdates
import numpy as np 
import os
import string
import re
from collections import OrderedDict
from itertools import repeat
from collections import defaultdict

f = open("data.txt", "r")


holder = f.read()


holder = [x for x in  re.split(r'(.*?\s.*?\s.*?)\s', holder) if x]

#print(holder)

dates = []
values = []
sorted_values = []
sorted_dates = []

for holder in holder:
	dates.append(holder.split(" ", maxsplit=1)[0] + " " + holder.split(" ", maxsplit=2)[2])

#print(dates)
n = len(dates)

dates_dict = defaultdict(float)


for dat in dates:
		date, float_str = dat.split(" ")
		dates_dict[date] += float(float_str)/2
sorted_values.append(['{} {}'.format(date, total) for date, total in dates_dict.items()])



for x in dates:
    if x.split(" ", maxsplit=1)[0] not in sorted_dates:
      sorted_dates.append(x.split(" ", maxsplit=1)[0])
 		
sorted_dates.sort()


for x in sorted_dates:
		if x.split(" ", maxsplit=1)[0] in sorted_values:
			print("domes")
			
sorted_values.sort(key = lambda x: x.split()[1])
print(sorted_dates)
print(sorted_values)





dateArray = []
time = dt.datetime.now()
for x in range(int(time.strftime("%d"))):
	if(x > 0):
		if(x < 10):
			dateArray.append(time.strftime("%m")+"/" +"0"+ str(x) + "/"+ time.strftime("%y"))
		else:
			dateArray.append(time.strftime("%m")+"/" + str(x) + "/"+ time.strftime("%y"))


#print(dateArray)




x = [dt.datetime.strptime(d,'%m/%d/%y').date() for d in dateArray]
y = range(len(dateArray))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator())


plt.plot(x,y)
plt.ylabel('Sentiment')
plt.xlabel('Time')
plt.gcf().autofmt_xdate()
plt.show()



#for k in sorted(ss):
	#	out.write('{0}: {1}, '.format(k, ss[k]))
