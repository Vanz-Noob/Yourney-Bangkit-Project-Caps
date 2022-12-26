#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tweepy
import csv
import string
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import seaborn as sns
from sklearn import model_selection
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.utils.multiclass import unique_labels
import seaborn as sns
import matplotlib.pyplot as plt


# In[ ]:


config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']
access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


# In[ ]:


def category_tweet_retriever(query):
    tweets = []
    
    for tweet in tweepy.Cursor(api.search_tweets, 
                               q=query, 
                               lang='id', 
                               tweet_mode="extended").items(1000):
        tweets.append([tweet.created_at, tweet.author.screen_name, tweet.full_text])
        
    return tweets


# In[ ]:


df_id = pd.read_csv("stopwords_id.txt", header=None)
stopwords_id = df_id[0].to_list()

df_en = pd.read_csv("stopwords_en.txt", header=None)
stopwords_en = df_en[0].to_list()

def clean_tweet(tweet):    
    import stopwordsiso as stopwords

    process = tweet.lower()
    process = process.split()
    process = [word for word in process if not process in stopwords_en]
    process = [word for word in process if not process in stopwords_id]
    process = " ".join(word for word in process)
    process = re.sub("'", "", process) # to avoid removing contractions in english
    process = re.sub("^rt ", "", process)
    process = re.sub("@[A-Za-z0-9_]+","", process)
    process = re.sub("#","", process)
    process = re.sub(r'http\S+', '', process)
    process = re.sub('[()!?]', ' ', process)
    process = re.sub('\[.*?\]',' ', process)
    process = re.sub("[^a-z0-9]"," ", process)
    return process


# In[ ]:


def clean_spaces(tweet):
    process = tweet
    process = process.split()
    process = " ".join(word for word in process)
    return process


# In[ ]:


def splitter(tweet):
    return tweet.split()


# In[ ]:


def user_tweet_retriever(username):
    tweets = []
    
    for tweet in api.user_timeline(id=username,
                                   count=1000,
                                   tweet_mode="extended"):
        tweets.append([tweet.created_at, tweet.full_text])
        
    return tweets


# # Data Retrieval

# ## Gunung

# In[ ]:


header = ["created_at", "author", "tweet"]
df_gunung = pd.DataFrame(category_tweet_retriever("gunung"), columns=header)


# In[ ]:


print(df_gunung.shape)
df_gunung.head()


# In[ ]:


df_gunung['tweet'] = df_gunung['tweet'].apply(lambda x: clean_tweet(x))
df_gunung['tweet'] = df_gunung['tweet'].apply(lambda x: clean_spaces(x))
df_gunung.head()


# ## Pantai

# In[ ]:


header = ["created_at", "author", "tweet"]
df_pantai = pd.DataFrame(category_tweet_retriever("pantai"), columns=header)


# In[ ]:


print(df_pantai.shape)
df_pantai.head()


# In[ ]:


df_pantai['tweet'] = df_pantai['tweet'].apply(lambda x: clean_tweet(x))
df_pantai['tweet'] = df_pantai['tweet'].apply(lambda x: clean_spaces(x))
df_pantai.head()


# In[ ]:


print(df_pantai["tweet"][2])


# ## Kuliner

# In[ ]:


header = ["created_at", "author", "tweet"]
df_kuliner = pd.DataFrame(category_tweet_retriever("kuliner"), columns=header)


# In[ ]:


print(df_kuliner.shape)
df_kuliner.head()


# In[ ]:


df_kuliner['tweet'] = df_kuliner['tweet'].apply(lambda x: clean_tweet(x))
df_kuliner['tweet'] = df_kuliner['tweet'].apply(lambda x: clean_spaces(x))
df_kuliner.head()


# # Dataset

# In[ ]:


# drop duplikat dulu, baru digabungin ke dataset
# pr aliif


# In[ ]:


df_gunung["category"] = "gunung"
df_pantai["category"] = "pantai"
df_kuliner["category"] = "kuliner"


# In[ ]:


df_gunung.head()


# In[ ]:


# sementara pakai ini dulu
# ke depannya gak pake csv
# ke depannya baca data dari database
unique = pd.read_csv("_dataset/dataset_unique 2022-11-01.csv")


# In[ ]:


# baca data dari database
# masuk jadi bentuk dataframe
# kode database dari cc di sini


# In[ ]:


df_all = pd.concat([unique, df_gunung, df_pantai, df_kuliner], ignore_index=True)
print("unique dataset length before:", len(unique))
print("unique dataset length after new data addition:", len(df_all))


# In[ ]:


df_all.head()


# In[ ]:


df_all = df_all.drop_duplicates(subset=['tweet'])
print("unique dataset length after duplicate removed:", len(df_all))


# In[ ]:


# append tweet yang baru
# pr coco


# # Naive Bayes Model

# In[ ]:


df_all = df_all.dropna()
df_all.info()


# In[ ]:


df_all['category'].value_counts()


# In[ ]:


yTarget = df_all["category"]
print(yTarget)


# In[ ]:


#test
Y = yTarget
print(Y)
print(Y.shape)


# In[ ]:


vectorizer = CountVectorizer(analyzer=splitter).fit(df_all["tweet"])
xTarget = vectorizer.transform(df_all["tweet"])
# print(vectorizer.vocabulary_)
print(len(vectorizer.vocabulary_))
print(xTarget.shape)


# In[ ]:


tfidf = TfidfTransformer()
X = tfidf.fit_transform(xTarget)
print(X.shape)


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=1)
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)


# In[ ]:


NaiveBayes = MultinomialNB().fit(X_train, np.ravel(y_train, order="C"))
print(NaiveBayes)


# In[ ]:


prediction = NaiveBayes.predict(X_test)
accuracies = accuracy_score(y_test, prediction)

print(prediction)
print(accuracies)


# In[ ]:


cf_matrix = confusion_matrix(y_test, prediction)
print(confusion_matrix(y_test, prediction))


# In[ ]:


labels = ["gunung", "pantai", "kuliner"]
sns.heatmap(cf_matrix, annot=True, cmap='Greys', fmt="d",
            xticklabels=labels, yticklabels=labels)


# # User Tweet Probability

# In[ ]:


X_dataset, y_dataset = X, Y

print(X_dataset.shape)
print(y_dataset.shape)


# In[ ]:


username = "aliifnrhmn"

header = ["created_at", "tweet"]
df_user = pd.DataFrame(user_tweet_retriever(username), columns=header)
df_user['tweet'] = df_user['tweet'].apply(lambda x: clean_tweet(x))
df_user['tweet'] = df_user['tweet'].apply(lambda x: clean_spaces(x))
df_user.head()


# In[ ]:


for i in range(len(df_user)):
    if df_user['tweet'][i] == '':
        df_user = df_user.drop(i, axis=0)


# In[ ]:


print(len(df_user))
df_user.head()
print(userTarget[1])


# In[ ]:


userTarget = vectorizer.transform(df_user["tweet"])
tfidf = TfidfTransformer()
user = tfidf.fit_transform(userTarget)
print(user.shape)
print(user[1])


# In[ ]:


probability = NaiveBayes.predict_proba(user)
print(probability)


# In[ ]:


category0 = []
category1 = []
category2 = []
for i in range(len(probability)):
    category0.append(probability[i][0])
    category1.append(probability[i][1])
    category2.append(probability[i][2])

def average(list):
    return sum(list)/len(list)

avg0 = round(average(category0)*100, 2)
avg1 = round(average(category1)*100, 2)
avg2 = round(average(category2)*100, 2)

print("username:", username)
print("Probability of gunung category : " + avg0) + "%"
print("Probability of pantai category : " + avg1) + "%"
print("Probability of kuliner category: " + avg2) + "%"


# In[ ]:


keys = {0:avg0, 1:avg1, 2:avg2}
max_avg = keys[0]

for i in range(3):
    for avg in keys[i]:
        if avg > max_avg:
            max_avg = avg
            
category_key = get_key(max_avg)

