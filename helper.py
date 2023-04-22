from urlextract import URLExtract
import pandas as pd
from collections import Counter
import emoji
import re
import regex
import streamlit as st
from datetime import datetime


def fetchStats (selectedUser, dataFrame):
    if selectedUser != "Overall":
        dataFrame = dataFrame[dataFrame['user'] == selectedUser]
    totalMessages = dataFrame.shape[0]
    
    word=[]
    for message in dataFrame['message']:
        word.extend(message.split())
    totalWords = len(word)
    
    totalMedia = dataFrame[dataFrame['message'] == '<Media omitted>\n'].shape[0]
    
    extractor = URLExtract()
    urls = extractor.find_urls(" ".join(word))
    totalURL = len(urls)
    
    return totalMessages, totalWords, totalMedia, totalURL

def mostBusy (x):
    topChatter = x['user'].value_counts().head()
    topChatterPercent = round((x['user'].value_counts()/x.shape[0])*100, 2).reset_index().rename(columns={'index':"Name", 'user':'Percentage'})

    return topChatter, topChatterPercent

def mostCommon (selectedUser, x):
    if selectedUser != "Overall":
        x = x[x['user'] == selectedUser]
    #remove stopwords and group notifications
    withoutGN = x[x['user'] != 'default']
    withoutGNMedia = withoutGN[withoutGN["message"] != '<Media omitted>\n']

    stopWords = open("stopwords-hinglish.txt", "r").read()
    
    words = []

    for message in withoutGNMedia['message']:
        for word in message.lower().split():
            if word not in stopWords:
                words.append(word)
    
    mC = Counter(words).most_common(20)
    mostCommon = pd.DataFrame(mC)
    mostCommon = mostCommon.rename(columns={0: 'Message', 1: 'Frequency'})

    return mostCommon

def mostEmoji (selectedUser ,x):
    if selectedUser != 'Overall':
        x = x[x['user'] == selectedUser]
    emojis = []
    for message in x['message']:
        message_emojized = emoji.emojize(message, language='alias')
        emojis.extend([c for c in message_emojized if c in emoji.UNICODE_EMOJI['en']])

    emoji_counts = Counter(emojis)
    emoji_df = pd.DataFrame(list(emoji_counts.items()), columns=['Emoji', 'Count'])
    emoji_df['Emoji'] = emoji_df['Emoji'].apply(lambda x: emoji.emojize(x, language='alias'))
    emoji_df = emoji_df.sort_values('Count', ascending=False).reset_index(drop=True)


    return emoji_df

def monthlyTimeline (selectedUser, x):
    if selectedUser != "Overall":
        x = x[x['user'] == selectedUser]
    timeline = x.groupby(['year', 'monthNum', 'month']).count()['message'].reset_index()
    
    time = []
    for i in range (timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str (timeline['year'][i]))
    timeline['time'] = time
    return timeline

def dailyTimeline (selectedUser, x):
    if selectedUser != "Overall":
        x = x[x['user'] == selectedUser]
    x['onlyDate'] = pd.to_datetime(x['date']).dt.date
    dailyTimeline = x.groupby("onlyDate").count()['message'].reset_index()
    return dailyTimeline

def weekActivity (selectedUser, x):
    if selectedUser != "Overall":
        x = x[x['user'] == selectedUser]
    weekActivity = x.groupby("dayName").count()['message'].reset_index()
    return x['dayName'].value_counts(), weekActivity