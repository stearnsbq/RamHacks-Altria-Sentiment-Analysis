import nltk
import praw
import pprint
from praw.models import MoreComments

reddit = praw.Reddit(client_id='FAByrixdQPAv6g',
                     client_secret='cE39zEYOi3RC3krM-XTM8wrXHCw',
                     user_agent='sentiment analysis',
                     password = 'WEbyN4he423WEJN', username = 'SmartMost')

print(reddit.read_only) 

submissions = []
subreddit = reddit.subreddit('nike')
i = 0
for submission in subreddit.hot(limit = 100):
	if 'nike' in submission.title:
		submissions.append(submission.id)
		





submission = reddit.submission(id=submissions[2])
print(submission.title)

#top_level_comments = list(submission.comments)
all_comments = submission.comments.list()
#print(top_level_comments.body)

submission.comments.replace_more(limit=None)

for comment in submission.comments.list():
		print(comment.body)



#for submission in reddit.subreddit('nike').hot(limit=30):
 #   print(submission.title)



 