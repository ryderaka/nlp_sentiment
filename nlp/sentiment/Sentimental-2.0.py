
# coding: utf-8

# In[ ]:


import tweepy
from tweepy import OAuthHandler
import json
from tweepy import Stream
from tweepy.streaming import StreamListener
from pymongo import MongoClient

consumer_key = 'AYyGdEpBASKaeqS8OFiQIoqzE'
consumer_secret = '8tkwkPmlWr5Eep6xOKQxIkkaM23lFWmRXpxH3kx7J7pxLzReNB'
access_token = '2438536710-EKRyhl3l4XBe2bI1Uz7ZbBpl2JAP6kkjDHoN3cP'
access_secret = 'xHfiSoZDeOKYizRGhYUXoA3aLVF7bRmZdbOvuz3DLhPjL'

auth = OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_secret)

api = tweepy.API(auth)

class MyListener(StreamListener):
    def on_data(self, data):
        try:
            Client = MongoClient()
            db = Client.hate25july   #Database name
            db.tweet.insert(json.loads(data))
            with open('hate.csv','a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data")
        return True
    def on_error(self,status):
        print(status)
        return True
    
twitter_stream = Stream(auth,MyListener())
twitter_stream.filter(languages=["en"], track=["hate"])


# In[10]:


#create a dataframe of all tweets 
import json
import pandas as pd
#Initial FileName
fd=open("report.json",'r')    
df = pd.DataFrame()
for line in fd:
    tweet = pd.read_json(line)
    df = df.append(tweet)
fd.close()
df


# In[11]:


#First Pass Polarity
import re
def polarity(tweet):
    emoji_set = ['👿','😾','😡','😠','😧','😭','😱','🙀','😈','😟','😿','😕','😖','😰','😢','😞','😳','😨','😬','😮','😣','😫','😒','😩','😵','😥','😦','😁','😯','😷','😔','😓','😜','😑','😶','😐','😴','😝','😪','😆','😎','😛','😲','😊','😀','😽','😙','😗','😚','☺️','😌','😄','😼','😸','😃','😺','😅','😏','😻','😍','😇','😂','😹','😘','😉','😋','🤗','😤']
    st = []
    polarity_set = {'👿':-5,'😾':-5,'😡':-5,'😠':-4,'😧':-4,'😭':-4,'😱':-4,'🙀':-4,'😈':-4,'😟':-4,'😿':-2,'😕':-2,'😖':-2,'😰':-2,'😢':-2,'😞':-2,'😳':-2,'😨':-2,'😬':-2,'😮':-2,'😣':-2,'😫':-2,'😒':-2,'😩':-2,'😵':-1,'😥':-1,'😦':-1,'😁':-1,'😯':-1,'😷':-1,'😔':-1,'😓':-1,'😜':-1,'😑':0,'😶':0,'😐':0,'😴':0,'😝':0,'😪':0,'😆':1,'😎':1,'😛':1,'😲':3,'😊':3,'😀':3,'😽':3,'😙':3,'😗':3,'😚':3,'☺️':3,'😌':3,'😄':3,'😼':3,'😸':3,'😃':3,'😺':3,'😅':3,'😏':3,'😻':4,'😍':4,'😇':4,'😂':4,'😹':4,'😘':4,'😉':4,'😋':4,'🤗':4,'😤':5}
    for i in tweet:
        if(i in str(emoji_set)):
            st.append(i)
        else:
            st.append('😑')
    st = [i.strip(' ') for i in st]   
    a = set(st)
    a = list(a)
    a = a[1:len(a)]
    pole_sum = 0
    s = tweet
    s = re.sub(r'[^\w\s]','',s)
    b = str(a)
    b = b.replace(',','')
    b = b.replace('[','')
    b = b.replace(']','')
    b = b.replace('\'','')
    b = b.replace('"','')
    for i in b:
        pole_sum += polarity_set.get(i,0)
    wr = s.strip() + ',' + b.strip() + ',' + str(pole_sum).strip() + '\n'
    refine = open("internal.csv",'a')
    refine.write(wr)
    refine.close()
   


# In[12]:


df1 = pd.DataFrame(list(df['text']))
#df1


# In[13]:


for i in range(len(df1)):
    polarity(str(df1[0][i]))
    


# In[ ]:


pwd


# In[16]:


import csv
refine_df = pd.read_excel("internal.xlsx",header=None)
refine_df = refine_df.dropna()
refine_df = refine_df.drop_duplicates()
refine_df.to_csv("first_pass_result.csv")


# In[15]:


refine_df = refine_df.reset_index()
refine_df

