from urlextract import URLExtract
import pandas as pd
from collections import Counter
import emoji

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
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emojiDF = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emojiDF
