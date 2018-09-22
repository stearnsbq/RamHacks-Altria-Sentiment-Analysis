import nltk
from string import punctuation
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.corpus import stopwords 
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

f = open("dataholder.txt", "r")

holder = f.read()
holder = holder.lower()
#print(holder)





setToken = sent_tokenize(holder)
worToken = word_tokenize(holder)



#print(setToken)
clean_tokens = []
sr = set(stopwords.words('english') + list(punctuation))
#print(sr)

for token in worToken:
	if token not in sr:
		clean_tokens.append(token)

#clean_tokens = filter(lambda x: x not in stopwords.words('english'), worToken)


sid = SentimentIntensityAnalyzer()

for sentence in setToken:
	#print(sentence)
	ss = sid.polarity_scores(sentence)
	for k in sorted(ss):
		print('{0}: {1}, '.format(k, ss[k]), end='')
	print()
