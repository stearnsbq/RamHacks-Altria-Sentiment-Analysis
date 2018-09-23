import praw
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import datetime as dt
from datetime import datetime
import numpy as np
import pandas as pd
from tkinter import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import *
from matplotlib.figure import Figure

# Ramhacks 2018 Altria Project: Sentinment Analysis of a Brand or Name on Social Media(Reddit)
# Uses Praw API to scrape a subreddit's posts and comments based on the args passed in from
# the GUI, using this data the program calculates sentinment using Natural Language Toolkit's
# bulit in API Vader which uses pre trained data to determine the polarity of a comment or 
# post content(if it's a text post)
#---------------------------------------
#	@Authors Byron Stearns, Timothy Patterson



# main class used to pull in data from reddit and use 2 temporary text files to sort and run vader API
class mclass:




# Intializes the GUI for the program to display the graph, and 
# to take in data from entry textfields
# @Param self - sets the root gui directory
# @Param root - root directory for gui


	def __init__(self, root):
		self.root = root
		
		root.title("Reddit Scrape")
		
		
		self.l1=Label(root,text="Subreddits to Search")
		self.l2=Label(root,text="Keyword to Search")   #Titles for gui elements
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


# Creates a graph based off the data found from the scraper
# and attaches it to the gui
# @Param self - gui


		
	def plot (self):
		
		file = open("data.txt", "r")
		holder = file.read()
		
		holder = [x for x in  re.split(' ', holder) if x] 
		
		dates = []
		values = []

		

		for x in range(int(len(holder)/3)):
			dates.append(holder[(3*x)])
		dates=[re.compile(r"-").sub("", m) for m in dates]   #pulls in dates from data file and formats accordingly
		for x in range(int(len(holder)/3)):
			values.append(float(holder[(3*x)+2]))
	
		
		dates.sort()
		values.sort()
		x = [datetime.strptime(d, '%Y%m%d').strftime('%m/%d/%Y') for d in dates]   #sets x axis to the dates 
		
		fig = Figure(figsize=(6,6))
		a = fig.add_subplot(111)
		a.scatter(x,values)
		a.set_title ("Estimation Grid", fontsize=16)
		a.set_ylabel("Sentiment", fontsize=14)
		a.set_xlabel("Date", fontsize=14)
		
		a.set_xticks(x[::25]) 
		
		canvas = FigureCanvasTkAgg(fig, master=self.root)
		canvas.get_tk_widget().pack()
		canvas.draw()
		
# Creates a new textfile and writes to the textfile the info obtained from the scraper
# @Param self - data from the textfields



	def run(self):
		file_input = open('input.txt', 'w')

		file_input.write(self.e1.get())
		file_input.write("\n")
		file_input.write(self.e2.get())    #Write to file the values pulled in from GUI
		file_input.write("\n")
		file_input.write(self.e3.get())
		file_input.close()
		
		
		reddit = praw.Reddit(client_id='CLIENT_ID',        #OAuth Call  
						client_secret="CLIENT_SECRET",
						user_agent='USER_AGENT')
					 
		file_input = open('input.txt', 'r')
	
		sin = file_input.read()   #Read from file and sort
		sf = sin.split('\n')
		sub_name = sf[0]
		sub_search = sf[1]
		limit_num = int(float(sf[2]))

		subreddit = reddit.subreddit(sub_name)   # subreddit instances

		data_subreddit = subreddit.search(sub_search,limit=limit_num)

		file_data = open("data.txt", 'w')  #New file to write data obtained from PRAW api and args passed from gui

		for submission in data_subreddit:  #for loop that runs through each submission in subreddit instance
	
			def get_date(created):
				return dt.datetime.fromtimestamp(created)
	
	
			dataT=submission.title  #Submission Title
			dataB=submission.selftext  #Submission Body Text
			dataC=submission.comments.list()  #Submission Comments
			dataD=submission.created #Submission Timestamp when comment is create 
			dataTD=get_date(dataD)  #Gets the data from the created instance
	
			file_data.write(" ")
			file_data.write(str(dataTD))  #writes data found to disk
			file_data.write(" ")
	
			sid = SentimentIntensityAnalyzer()   #Vader API call to determine the sentimental value of a comment or body text
			infull = ""
			infullc = ""
		
			infull += dataT
			if dataB != "":
				infull += " "
				infull += dataB
	
			submission.comments.replace_more()
			l = submission.comments.list()    #Grabs all replies 
			for x in range(len(l)):
				infullc += l[x].body
				infullc += " "
	
			infullc = infullc.lower() # makes sure each submission is lower case to ensure acurate comparasion
	
			setToken = sent_tokenize(infull)   #tokenizes comments
			setTokenc = sent_tokenize(infullc)
	
			ogpost_score = 0
			total_score = 0
			counter = 0
	
			for sen in setToken:
				ss=sid.polarity_scores(sen)
				s=ss['compound']     # Calculates sentiment values using sid/vader api
		
				ogpost_score += s
				total_score += s
				counter += 1
		
			print(ogpost_score)
			for sen in setTokenc:
				ss=sid.polarity_scores(sen)      #Calculates sentinment for body text and if the body text is negative negate all comment values
				s=ss['compound']
				if ogpost_score < 0:
					s = -s
				if s == 0.0:
					continue
				total_score += s
				counter += 1
	
			average_score = total_score / counter  # take average
			file_data.write(str(average_score))   # write the average to a text file

		file_data.close()
		self.plot()   #plot method call
	
	
	

	
	
	
root=Tk()
start=mclass(root)
mainloop()
