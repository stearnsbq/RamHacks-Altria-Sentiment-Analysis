import praw
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import datetime as dt
from datetime import datetime
import numpy as np
import pandas as pd
from tkinter import *
import matplotlib 
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import *
from matplotlib.figure import Figure

class mclass:
	def __init__(self, root):
		self.root = root
		
		root.title("Reddit Scrape")
		
		
		self.l1=Label(root,text="Subreddits to Search")
		self.l2=Label(root,text="Keyword to Search")
		self.l3=Label(root,text="Max Number of Entries")
		self.e1 = Entry(root, width = 40)
		self.e2 = Entry(root, width = 40)
		self.e3 = Entry(root, width = 40)

		self.t1 = self.e1.get()
		self.t2 = self.e2.get()
		self.t3 = self.e3.get()

		self.l1.pack()
		self.e1.pack()
		self.l2.pack()
		self.e2.pack()
		self.l3.pack()
		self.e3.pack()

		self.e1.focus_set()
		
		b=Button(root, text="Run", width=20, command = self.run)
		b.pack()


	def smooth(self, values):

		result = dict()

		for i in range(len(values)):
			result[values[i][0]] = np.array([]);
			for j in range(len(values)):
				if(values[i][0] == values[j][0]):
					result[values[i][0]] = np.append(result[values[i][0]], [float(values[j][1])])

		for key in result:
			result[key] = result[key].mean()


		return result



		
	def plot (self):
		
		file = open("data.txt", "r")
		holder = file.read()

		holder = re.split('\n', holder)
		
		dates = []
		values = []

		
		for x in holder:
			if(len(x) <= 0):
				continue
			val = x.split(' ')
			dates.append(val[0])
			values.append(val[2])


		sorted_values = [[date, x] for date, x in sorted(zip(dates,values))]

		sorted_values = self.smooth(sorted_values)

		
		x = list(sorted_values.keys())
		y = list(sorted_values.values())


		plt.plot(x, y, color='green', marker='o')
			

		plt.show()
		

	def run(self):
		
		reddit = praw.Reddit(client_id='SU3DL2_kxAdtqw',
						client_secret="hq0dRanTH4gmFcN4tfbFXcAcKeA",
						user_agent='RamhacksMW')
					 
		file_input = open('input.txt', 'r')
	
		sin = file_input.read()
		sf = sin.split('\n')
		sub_name = sf[0]
		sub_search = sf[1]
		limit_num = int(float(sf[2]))

		subreddit = reddit.subreddit(self.e1.get())

		data_subreddit = subreddit.search(self.e2.get(),limit=int(self.e3.get()))


		file_data = open("data.txt", 'w')

		for submission in data_subreddit:
			def get_date(created):
				return dt.datetime.fromtimestamp(created)
	
	
			dataT=submission.title
			dataB=submission.selftext
			dataC=submission.comments.list()
			dataD=submission.created
			dataTD=get_date(dataD)
	
			file_data.write(str(dataTD) + " ")
	
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
			file_data.write(str(average_score) + "\n")

		file_data.close()
		self.plot()
	
	
	

	
	
	
root=Tk()
start=mclass(root)


mainloop()
