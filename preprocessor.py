import re
import pandas as pd
import streamlit as st


def preprocess(data):
    # creating a regex equation that matches the date and time format in the given message
    pattern = '\d{2}\/\d{2}\/\d{2}, \d{1,2}:\d{2}\s(?:am|pm) - '
    # extracting messages on the basis of 'regex' pattern
    messages = re.split(pattern, data)[1:]
    # extracting date&time on the basis of 'regex' pattern
    dates = re.findall(pattern, data)
    # replacing the \u202f character with a space in the dates list
    dates = [date.replace('\u202f', ' ') for date in dates]
    # converting to a pandas dataframe
    x = pd.DataFrame({"messages": messages, "date": dates})
    # converting the "date" type
    x["date"] = pd.to_datetime(x['date'], format='%d/%m/%y, %I:%M %p - ')
    # converting time to 24-hour format and updating the "dates" column
    x["date"] = x["date"].dt.strftime('%Y-%m-%d %H:%M:%S')
    # splitting the "messages" column into "user" and "message" columns
    x[['user', 'message']] = x['messages'].str.split(': ', 1, expand=True)

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
    return x
