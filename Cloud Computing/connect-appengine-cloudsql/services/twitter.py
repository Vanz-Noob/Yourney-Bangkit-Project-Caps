#!/usr/bin/env python

import os
import tweepy
import pandas as pd
import numpy as np
import re
import configparser
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix
from dataset import DatasetService
from user import UserService

# Functions
config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']
access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

df_id = pd.read_csv("stopwords_id.txt", header=None)
stopwords_id = df_id[0].to_list()

df_en = pd.read_csv("stopwords_en.txt", header=None)
stopwords_en = df_en[0].to_list()

def category_tweet_retriever(query):
    tweets = []
    
    for tweet in tweepy.Cursor(api.search_tweets, 
                               q=query, 
                               lang='id', 
                               tweet_mode="extended").items(1):
        tweets.append([tweet.created_at, tweet.author.screen_name, tweet.full_text])
    return tweets

def clean_tweet(tweet):
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

def clean_spaces(tweet):
    process = tweet
    process = process.split()
    process = " ".join(word for word in process)
    return process

def splitter(tweet):
    return tweet.split()

def user_tweet_retriever(username):
    tweets = []
    
    for tweet in api.user_timeline(id=username,
                                   count=2000,
                                   tweet_mode="extended"):
        tweets.append([tweet.created_at, tweet.full_text])
        
    return tweets

def average(list):
    return sum(list)/len(list)

def update_dataset():
    header = ["created_at", "author", "tweet"]

    # Gunung
    df_gunung = pd.DataFrame(category_tweet_retriever("gunung"), columns=header)
    df_gunung['tweet'] = df_gunung['tweet'].apply(lambda x: clean_tweet(x))
    df_gunung['tweet'] = df_gunung['tweet'].apply(lambda x: clean_spaces(x))


    # Pantai
    df_pantai = pd.DataFrame(category_tweet_retriever("pantai"), columns=header)
    df_pantai['tweet'] = df_pantai['tweet'].apply(lambda x: clean_tweet(x))
    df_pantai['tweet'] = df_pantai['tweet'].apply(lambda x: clean_spaces(x))

    # Kuliner
    df_kuliner = pd.DataFrame(category_tweet_retriever("kuliner"), columns=header)
    df_kuliner['tweet'] = df_kuliner['tweet'].apply(lambda x: clean_tweet(x))
    df_kuliner['tweet'] = df_kuliner['tweet'].apply(lambda x: clean_spaces(x))

    # Dataset
    df_gunung["category"] = "gunung"
    df_pantai["category"] = "pantai"
    df_kuliner["category"] = "kuliner"

    # sementara pakai ini dulu
    # ke depannya gak pake csv
    # ke depannya baca data dari database

    # unique = pd.read_csv("_dataset/dataset_unique 2022-11-01.csv")
    # df_all = pd.concat([unique, df_gunung, df_pantai, df_kuliner], ignore_index=True)
    df_all = pd.concat([df_gunung, df_pantai, df_kuliner], ignore_index=True)
    df_all = df_all.drop_duplicates(subset=['tweet'])

    # baca data dari database
    # masuk jadi bentuk dataframe
    # kode database dari cc di sini

    # append tweet yang baru
    # pr coco

    # Naive Bayes Model
    df_all = df_all.dropna()
    dict_of_dataset = df_all.to_dict('records')
    return dict_of_dataset

def average_data(username,data):
    try:
        df_all = pd.DataFrame.from_dict(data)

        yTarget = df_all["category"]
        encoder = LabelEncoder()
        Y = encoder.fit_transform(yTarget)

        vectorizer = CountVectorizer(analyzer=splitter).fit(df_all["tweet"])
        xTarget = vectorizer.transform(df_all["tweet"])
        tfidf = TfidfTransformer()
        X = tfidf.fit_transform(xTarget)

        X_train, X_test, y_train = train_test_split(X, Y, test_size=0.2, random_state=1)
        NaiveBayes = MultinomialNB().fit(X_train, np.ravel(y_train, order="C"))

        # User Tweet Probability

        header = ["created_at", "tweet"]
        df_user = pd.DataFrame(user_tweet_retriever(username), columns=header)
        df_user['tweet'] = df_user['tweet'].apply(lambda x: clean_tweet(x))
        df_user['tweet'] = df_user['tweet'].apply(lambda x: clean_spaces(x))

        for i in range(len(df_user)):
            if df_user['tweet'][i] == '':
                df_user = df_user.drop(i, axis=0)

        userTarget = vectorizer.transform(df_user["tweet"])
        tfidf = TfidfTransformer()
        user = tfidf.fit_transform(userTarget)
        probability = NaiveBayes.predict_proba(user)

        category0 = []
        category1 = []
        category2 = []
        for i in range(len(probability)):
            category0.append(probability[i][0])
            category1.append(probability[i][1])
            category2.append(probability[i][2])


        avg0 = round(average(category0)*100, 2)
        avg1 = round(average(category1)*100, 2)
        avg2 = round(average(category2)*100, 2)

        data = {avg0:0, avg1:1, avg2:2}
        keys = data.keys()
        max_keys = max(keys)
        return data[max_keys]

    except Exception as e:
        return e

if __name__ == '__main__':
    newData = update_dataset()
    db_user = os.environ.get('CLOUD_SQL_USERNAME')
    db_password = os.environ.get('CLOUD_SQL_PASSWORD')
    db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
    db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')
    data_service = DatasetService(db_user,db_password,db_name,db_connection_name)
    user_service = UserService(db_user,db_password,db_name,db_connection_name)

    for data in newData:
        if 'categori' not in data:
            continue
        if len(data['categori']) > 0 or len(data['author']) > 0 or len(data['created_at']) > 0 or len(data['tweet']) > 0 :
            data_service.add_dataset(data['created_at'],data['author'], data['categori'], data['tweet'])
        else:
            continue
    
    current_data = data_service.get_dataset_by_kategori()
    
    null = user_service.user_kategori_null()

    for user in null:
        try:
            id_kategori = average_data(user['username_twitter'], current_data)
            user_service.user_update_kategori(id_kategori)
            user['id_kategori'] = id_kategori
            user['status'] = 'success'
        except Exception as e:
            user['status'] = 'failed with error::' + str(e)
            continue

