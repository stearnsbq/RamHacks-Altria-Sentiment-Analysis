import nltk
import praw
import pprint
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from praw.models import MoreComments

reddit = praw.Reddit(client_id='FAByrixdQPAv6g',
                     client_secret='cE39zEYOi3RC3krM-XTM8wrXHCw',
                     user_agent='sentiment analysis',
                     password = 'WEbyN4he423WEJN', username = 'SmartMost')

print(reddit.read_only) 
comments = []
title = []
submissions = []
f = open("dataholder.txt", "w")
subreddits = ['politics','nike','shoes']
subreddit = reddit.subreddit('politics')
i = 0

for subname in subreddits:
	subreddit = reddit.subreddit(subname)
	for submission in subreddit.hot(limit = 1000):
		if 'Kaepernick' in submission.title:
			submissions.append(submission.id)
		





	for x in range(len(submissions)):	
		submission = reddit.submission(id=submissions[x])
		f.write("Title: \n")
		f.write(submission.title + "\n")

#top_level_comments = list(submission.comments)
		all_comments = submission.comments.list()
#print(top_level_comments.body)

		f.write("Comments: \n")
		submission.comments.replace_more(limit=None)
		for comment in submission.comments.list():
			f.write(comment.body + "\n")
	f.write("\n")









#for submission in reddit.subreddit('nike').hot(limit=30):
 #   print(submission.title)



 