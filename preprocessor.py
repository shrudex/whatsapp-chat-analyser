import re
import pandas as pd
import streamlit as st


def preprocess(data):
    
    # creating a regex equation that matches the date and time format in the given message
    #pattern = '\d{2}\/\d{2}\/\d{2}, \d{1,2}:\d{2}\s(?:am|pm) - '
    # extracting messages on the basis of 'regex' pattern
    #messages = re.split(pattern, data)[1:]
    # extracting date&time on the basis of 'regex' pattern
    #dates = re.findall(pattern, data)
    # replacing the \u202f character with a space in the dates list
    #dates = [date.replace('\u202f', ' ') for date in dates]
    # converting to a pandas dataframe
    #x = pd.DataFrame({"messages": messages, "date": dates})
    # converting the "date" type
    #x["date"] = pd.to_datetime(x['date'], format='%d/%m/%y, %I:%M %p - ')
    # converting time to 24-hour format and updating the "dates" column
    #x["date"] = x["date"].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    pattern = '\d{2}\/\d{2}\/\d{2}, \d{1,2}:\d{2}\s(?:am|pm) - '
    regex = r'\d{2}/\d{2}/\d{4}, \d{1,2}:\d{2}\s*[ap]m'
    regexN = r'\d{1,2}\/\d{1,2}\/\d{2},\s\d{1,2}:\d{2}\s[AP]M'


    dates1 = re.findall(regex, data)
    dates2 = re.findall(pattern, data)
    dates3 = re.findall(regexN, data)

    regex = r'\d{2}/\d{2}/\d{4}, \d{1,2}:\d{2}\s*[ap]m - '
    regexN = r'\d{1,2}\/\d{1,2}\/\d{2},\s\d{1,2}:\d{2}\s[AP]M\s-\s'

    messages1 = re.split(regex, data)[1:]
    messages2 = re.split(pattern, data)[1:]
    messages3 = re.split(regexN, data)[1:]
    
    holdsZero = [0, len(dates1), len(dates2), len(dates3)]
    dates = dates2
    messages = messages2
    if (holdsZero[1]):
        dates = dates1
        messages = messages1
    if (holdsZero[3]):
        dates = dates3
        messages = messages3
    dates = [date.replace('\u202f', ' ') for date in dates]
    
    x = pd.DataFrame({"messages":messages, "date":dates})
    #converting the "date" type
    if (holdsZero[1]):
        x["date"] = pd.to_datetime(x['date'], format="%d/%m/%Y, %I:%M %p")
        x["date"] = x["date"].dt.strftime('%Y-%m-%d %H:%M:%S')
    if (holdsZero[3]):
        x["date"] = pd.to_datetime(x['date'], format='%m/%d/%y, %I:%M %p')
        x["date"] = x["date"].dt.strftime('%Y-%m-%d %H:%M:%S')

    if (holdsZero[2]):
        x["date"] = pd.to_datetime(x['date'], format='%d/%m/%y, %I:%M %p - ')
        x["date"] = x["date"].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # splitting the "messages" column into "user" and "message" columns
    x[['user', 'message']] = x['messages'].str.split(': ', n=1, expand=True)


    # setting "default" user for messages without a sender
    x.loc[x['messages'].str.find(':') == -1, 'user'] = "default"

    # for the "default" case or messages without a colon, the "message" column will store the "messages"
    x.loc[x['messages'].str.find(':') == -1, 'message'] = x['messages']

    # for messages with a colon, split the message and store the user and message accordingly
    x.loc[x['messages'].str.find(
        ':') != -1, 'user'] = x['messages'].str.split(':').str[0]
    x.loc[x['messages'].str.find(
        ':') != -1, 'message'] = x['messages'].str.split(': ').str[1]

    # dropping the "messages" column
    x.drop('messages', axis=1, inplace=True)

    # reordering the columns
    x = x[['date', 'user', 'message']]

    # extracting year, month and day from "date" column and creating new columns
    x["year"] = pd.to_datetime(x["date"], format="%Y-%m-%d %H:%M:%S").dt.year.astype(str).str.zfill(4)
    
    #just for debugging 
    #st.dataframe(x)
    #st.title("after year in pre processor")
    
    x["month"] = pd.to_datetime(x["date"], format="%Y-%m-%d %H:%M:%S").dt.month_name()
    x['monthNum'] = pd.to_datetime(x['month'], format='%B').dt.month

    x["day"] = pd.to_datetime(x["date"], format="%Y-%m-%d %H:%M:%S").dt.day

    # extracting hour and minute from "date" column and creating new columns
    x['hour'] = pd.to_datetime(
        x["date"], format="%Y-%m-%d %H:%M:%S").dt.hour
    x['minute']  = pd.to_datetime(
        x["date"], format="%Y-%m-%d %H:%M:%S").dt.minute
    
    x['dayName'] = pd.to_datetime(x['date'], format="%Y-%m-%d %H:%M:%S").dt.day_name()
    x['monthName'] = pd.to_datetime(x['date'], format="%Y-%m-%d %H:%M:%S").dt.month_name()
    
    period = []
    for hour in x[['dayName', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour+1))
        else:
            period.append(str(hour) + "-" + str(hour+1))
    x['period'] = period
    
    x['replyTime'] = pd.to_datetime(x['date']).diff().fillna(pd.Timedelta(seconds=0))
    x = x[x['replyTime'] <= pd.Timedelta(days=2)]


    return x
