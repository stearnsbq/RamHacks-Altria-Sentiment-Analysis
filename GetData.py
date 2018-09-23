import praw
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd

reddit = praw.Reddit(client_id='SU3DL2_kxAdtqw',
                     client_secret="hq0dRanTH4gmFcN4tfbFXcAcKeA",
                     user_agent='RamhacksMW')
					 
file_input = open('input.txt', 'r')

sin = file_input.read()
sf = sin.split('\n')
sub_name = sf[0]
sub_search = sf[1]
limit_num = int(float(sf[2]))


subreddit = reddit.subreddit(sub_name)

data_subreddit = subreddit.search(sub_search,limit=limit_num)

file_data = open("data.txt", 'w')

for submission in data_subreddit:
	
	def get_date(created):
		return dt.datetime.fromtimestamp(created)
	
	
	dataT=submission.title
	dataB=submission.selftext
	dataC=submission.comments.list()
	dataD=submission.created
	dataTD=get_date(dataD)
	
	file_data.write("\n")
	file_data.write(str(dataTD))
	file_data.write("\n")
	
	sid = SentimentIntensityAnalyzer()
	infull = ""
	infullc = ""
	
	infull += dataT
	if dataB != "":
		infull += " "
		infull += dataB
	
	submission.comments.replace_more()
	l = submission.comments.list()
	for x in range(len(l)):
		infullc += l[x].body
		infullc += " "
	
	infullc = infullc.lower()
	
	setToken = sent_tokenize(infull)
	setTokenc = sent_tokenize(infullc)
	
	ogpost_score = 0
	total_score = 0
	counter = 0
	
	for sen in setToken:
		ss=sid.polarity_scores(sen)
		s=ss['compound']
		
		ogpost_score += s
		total_score += s
		counter += 1
		
	print(ogpost_score)
	for sen in setTokenc:
		ss=sid.polarity_scores(sen)
		s=ss['compound']
		if ogpost_score < 0:
			s = -s
		if s == 0.0:
			continue
		total_score += s
		counter += 1
	
	average_score = total_score / counter
	file_data.write(str(average_score))

file_data.close()