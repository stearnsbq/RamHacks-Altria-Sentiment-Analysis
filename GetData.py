import praw
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import datetime as dt

reddit = praw.Reddit(client_id='SU3DL2_kxAdtqw',
                     client_secret="hq0dRanTH4gmFcN4tfbFXcAcKeA",
                     user_agent='RamhacksMW')
					 
file_input = open('input.txt', 'r')

sin = file_input.read()
sf = sin.split('\n')
sub_name = sf[0]
limit_num = int(float(sf[1]))

subreddit_nike = reddit.subreddit(sub_name)

data_subreddit_nike = subreddit_nike.search('nike',limit=limit_num)

file_data_nike = open("data_nike.txt", 'w')

for submission in data_subreddit_nike:
	
	def get_date(created):
		return dt.datetime.fromtimestamp(created)
	
	
	dataT=submission.title
	dataB=submission.selftext
	dataC=submission.comments.list()
	dataD=submission.created
	dataTD=get_date(dataD)
	
	file_data_nike.write("\n")
	file_data_nike.write(str(dataTD))
	file_data_nike.write("\n")
	
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
		#file_data_nike.write("T")
		#file_data_nike.write(str(s))
		#file_data_nike.write('\n')
		ogpost_score += s
		total_score += s
		counter += 1
		#print(s)
		#print()
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
		#file_data_nike.write(str(s))
		#file_data_nike.write('\n')
		
		#print(s)
		#print()
	#file_data_nike.write("\n\n")
	average_score = total_score / counter
	file_data_nike.write(str(average_score))

file_data_nike.close()