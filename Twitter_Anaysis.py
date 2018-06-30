import time
from tweepy import Stream #'Tweepy' it is an API(Application Programming Interface) and 'Stream' would grab recent tweets
from tweepy import OAuthHandler #gives an authenticaction
from tweepy.streaming import StreamListener #gives callbeck when new tweet is posted
import json
from textblob import TextBlob
import matplotlib.pyplot as plt
import re

"# -- coding: utf-8 --"

def calctime(a): #calculate the difference from the time tweet is posted and the time this fuction works.
    return time.time()-a # Time when the post is tweeted minus time when the function is excecuted

positive = 0 #Good Emotions
negative = 0 #Bad Emotion
compound = 0 #Neutrial

initime = time.time()

count = 0
plt.ion() #It changes plot according to the time ("Interactive plot")

ckey='' #Consumer Key (API Key)
csecret='' #Consumer Secret (API Secret)
atoken='' #Access Token
asecret='' #Access Token Secret

class listener(StreamListener):

    def on_data(self,data):
        global initime;

        t = int(calctime(initime))

        all_data = json.loads(data)
        tweet = all_data["text"] #took al data and put in tweet
        tweet = " ".join(re.findall("[a-zA-Z]+",tweet)) #Reges Function thats only find words/strings and join with spaces with sapces

        blob = TextBlob(tweet.strip())

        global positive
        global negative
        global compound
        global count

        count=count+1
        senti=0

        for sen in blob.sentences:  #finds its sentiments
            senti=senti+sen.sentiment.polarity
            if sen.sentiment.polarity>=0:
                positive=positive+sen.sentiment.polarity
            else:
                negative=negative+sen.sentiment.polarity
        compound=compound+senti

        print(count)
        print(tweet.strip())
        print(senti)
        print(t)
        print(positive,negative,compound)

        plt.axis([0,70,-20,20]) #Ploting tweet vs time
        plt.xlabel('Time')
        plt.ylabel('Sentiment')
        plt.plot([t],[positive],'go',[t],[negative],'ro',[t],[compound],'bo') #Positive with green, negative with red and compound with grey
        plt.show()
        plt.pause(0.0001)
        if count==200:
            return False
        else:
            return True

    def on_error(self,status):
        print(status)

auth = OAuthHandler(ckey,csecret)
auth.set_access_token(atoken,asecret)

searchTerm = input("Enter Keyword/Tag to search about: ")
NoOfTerms= int(input("Enter how many tweets you want to see"))

twitterStream = Stream(auth,listener(NoOfTerms))
twitterStream.filter(track=[searchTerm])
