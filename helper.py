from urlextract import URLExtract
import pandas as pd
from collections import Counter
import emoji
import re
import regex
import streamlit as st
from datetime import datetime


def fetchStats(selectedUser, dataFrame):
    if selectedUser != "Overall":
        dataFrame = dataFrame[dataFrame['user'] == selectedUser]
    totalMessages = dataFrame.shape[0]

    word = []
    for message in dataFrame['message']:
        if isinstance(message, str):
            word.extend(message.split())
    totalWords = len(word)

    totalMedia = dataFrame[dataFrame['message']
                           == '<Media omitted>\n'].shape[0]

    extractor = URLExtract()
    urls = extractor.find_urls(" ".join(word))
    totalURL = len(urls)

    return totalMessages, totalWords, totalMedia, totalURL


def mostBusy(x):
    topChatter = x['user'].value_counts().head()
    topChatterPercent = round((x['user'].value_counts(
    )/x.shape[0])*100, 2).reset_index().rename(columns={'index': "Name", 'user': 'Percentage'})

    return topChatter, topChatterPercent


def mostCommon(selectedUser, x):
    if selectedUser != "Overall":
        x = x[x['user'] == selectedUser]
    # remove stopwords and group notifications
    withoutGN = x[x['user'] != 'default']
    withoutGNMedia = withoutGN[withoutGN["message"] != '<Media omitted>\n']

    stopWords = open("stopwords-hinglish.txt", "r").read()

    words = []

    for message in withoutGNMedia['message']:
        if isinstance(message, str):
            for word in message.lower().split():
                if word not in stopWords:
                    words.append(word)

    mC = Counter(words).most_common(20)
    mostCommon = pd.DataFrame(mC)
    mostCommon = mostCommon.rename(columns={0: 'Message', 1: 'Frequency'})

    return mostCommon


def mostEmoji(selectedUser, x):
    if selectedUser != 'Overall':
        x = x[x['user'] == selectedUser]
    emojis = []
    for message in x['message']:
        if isinstance(message, str):
            message_emojized = emoji.emojize(message, language='alias')
            emojis.extend(
                [c for c in message_emojized if c in emoji.UNICODE_EMOJI['en']])

    emoji_counts = Counter(emojis)
    emoji_df = pd.DataFrame(list(emoji_counts.items()),
                            columns=['Emoji', 'Count'])
    emoji_df['Emoji'] = emoji_df['Emoji'].apply(
        lambda x: emoji.emojize(x, language='alias'))
    emoji_df = emoji_df.sort_values(
        'Count', ascending=False).reset_index(drop=True)

    return emoji_df


def monthlyTimeline(selectedUser, x):
    if selectedUser != "Overall":
        x = x[x['user'] == selectedUser]
    timeline = x.groupby(['year', 'monthNum', 'month']).count()[
        'message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline


def dailyTimeline(selectedUser, x):
    if selectedUser != "Overall":
        x = x[x['user'] == selectedUser]
    x['onlyDate'] = pd.to_datetime(x['date']).dt.date
    dailyTimeline = x.groupby("onlyDate").count()['message'].reset_index()
    return dailyTimeline


def weekActivity(selectedUser, x):
    if selectedUser != "Overall":
        x = x[x['user'] == selectedUser]
    weekActivity = x.groupby("dayName").count()['message'].reset_index()
    return x['dayName'].value_counts(), weekActivity


def monthActivity(selectedUser, x):
    if selectedUser != "Overall":
        x = x[x['user'] == selectedUser]
    monthActivity = x.groupby("monthName").count()['message'].reset_index()
    return x['monthName'].value_counts(), monthActivity


def hourActivity(selectedUser, x):
    if selectedUser != "Overall":
        x = x[x['user'] == selectedUser]
    return x.groupby(['dayName', 'hour'])['message'].count(), x.groupby(['dayName', 'hour'])['message'].count().reset_index()



def messageExtractor (selectedUser, x, inputDate):
    #inputDate = "20-04-2023"
    if selectedUser != "Overall":
        x = x[x['user'] == selectedUser]
    if (len(inputDate)==10):
        dd = inputDate[0:2]
        mm = inputDate[3:5]
        yyyy = inputDate[6:]
        if (dd[0]=='0'): dd = dd[1]
        if (mm[0]=='0'): mm = mm[1]
        mask = (x['day'].astype(str) == dd) & (x['monthNum'].astype(str) == mm) & (x['year'].astype(str) == yyyy)
        messageExtract = pd.DataFrame(x[mask])[['user', 'message']]
        if (messageExtract.shape[0]>0):
            messageExtract['time'] = x['hour'].astype(str) + ':' + x['minute'].astype(str)
            messageExtract['message'] = messageExtract['message'].str.replace('\n', '')
        #st.dataframe(messageExtract)

        return messageExtract

def activity (selectedUser, x):
    if selectedUser != "Overall":
        x = x[x['user'] == selectedUser]
    activityX = x.groupby("period").count()['message'].reset_index()
    return activityX

def replyTime (selectedUser, x):
    timeSelected = pd.Timedelta(0)
    timeDifference = x.groupby('user')['replyTime'].mean().reset_index().sort_values('replyTime', ascending=True).head(5)
    timeDifference = timeDifference[timeDifference['user'] != 'default']
    if selectedUser != "Overall":
        x = x[x['user'] == selectedUser]
        timeSelected = timeDifference[timeDifference['user'] == selectedUser]['replyTime'].iloc[0]

    return timeDifference, timeSelected
