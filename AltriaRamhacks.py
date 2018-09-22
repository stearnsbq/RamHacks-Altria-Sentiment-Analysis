import praw

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
	dataT=""
	dataB=""
	
	dataT=submission.title
	dataB=submission.selftext
	
	try:
		file_data_nike.write("Title: \n")
		file_data_nike.write(dataT)
		file_data_nike.write("\n")
	except:
		print("Error")

	if dataB != "":
		try:
			file_data_nike.write("Body: \n")
			file_data_nike.write(dataB)
			file_data_nike.write("\n")
		except:
			print("Error")
	file_data_nike.write("Comments: \n")
	submission.comments.replace_more()
	l = submission.comments.list()

	for x in range(len(l)):
		try:
			file_data_nike.write(l[x].body)
			file_data_nike.write("\n")
		except:
			print("Error")
file_data_nike.close()