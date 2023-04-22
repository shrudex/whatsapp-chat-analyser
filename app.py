import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import emoji
import seaborn as sns
import plotly.express as px


st.set_page_config(page_title="Shrudex", layout="wide")

st.title("WhatsApp Chat Analyzer🔎")
st.write("Made with❤️‍🔥 by Shrudex!👨🏻‍💻")

st.sidebar.title("WhatsApp Chat Analyzer")
uploadedFile = st.sidebar.file_uploader("Choose a File🗃️")
if uploadedFile is not None:
    bytesData = uploadedFile.getvalue()
    finalData = bytesData.decode("utf-8")
    dataFrame = preprocessor.preprocess(finalData)
    st.title("WhatsApp Chat Data")
    st.dataframe(dataFrame.head())

    # fetch unique users
    userList = dataFrame["user"].unique().tolist()
    userList.remove("default")
    userList.sort()
    userList.insert(0, "Overall")
    selectedUser = st.sidebar.selectbox("Show Analysis🤔 WRT", userList)

    if st.sidebar.button("Show Analysis🔢"):
        # statistics
        numMessages, numWords, numMedia, numURL = helper.fetchStats(
            selectedUser, dataFrame)
        st.title("Top Statistics📈")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages🤳🏻")
            st.title(numMessages)
        with col2:
            st.header("Total Words💭")
            st.title(numWords)
        with col3:
            st.header("Media Shared🎥")
            st.title(numMedia)
        with col4:
            st.header("Links Shared🔗")
            st.title(numURL)
            
        #monthly timeline
        st.title("Monthly Timeline⌚")
        timeline = helper.monthlyTimeline(selectedUser, dataFrame)
        plt.style.use('dark_background')
        plt.figure(figsize=(12, 3)) 
        plt.plot(timeline['time'], timeline['message'])
        plt.xticks(rotation='vertical')
        plt.title(f"{selectedUser}", color='yellow')
        st.pyplot(plt)
        
        #daily timeline
        st.title("Daily Timeline📅")
        dailyTimeline = helper.dailyTimeline (selectedUser, dataFrame)
        plt.style.use('dark_background')
        plt.figure(figsize = (14, 3))
        plt.plot(dailyTimeline['onlyDate'], dailyTimeline['message'])
        plt.xticks(rotation='vertical')
        plt.title('Daily Message Count', color='yellow')
        plt.xlabel('Date', color='white')
        plt.ylabel('Message Count', color='white')
        st.pyplot(plt)
        
        #activity map
        st.title("Week Activity")
        weekActivitySeries, weekActivity = helper.weekActivity (selectedUser, dataFrame)
        fig = px.pie(weekActivity, values='message', names='dayName', hole=0.6, color_discrete_sequence=px.colors.qualitative.Dark2)
        fig.update_layout(template='plotly_dark')
        st.plotly_chart(fig)



        # finding busiest users in the group
        if selectedUser == 'Overall':
            st.header("Top Chatters🗣️")
            topChatter, topChatterPercent = helper.mostBusy(dataFrame)
            col1, col2 = st.columns(2)

            with col1:
                plt.style.use('dark_background')
                name = topChatter.index
                name = [emoji.emojize(n) for n in name]
                count = topChatter.values
                fig, ax = plt.subplots()
                plt.xlabel('Name').set_color('yellow')
                plt.ylabel('Messages Sent').set_color('yellow')
                ax.bar(name, count, width=0.8)
                plt.xticks(rotation='vertical')
                ax.tick_params(axis='both', which='major', labelsize=8)

                st.pyplot(fig)

            with col2:
                st.dataframe(topChatterPercent)

        # most common words
        
        mostCommon = helper.mostCommon(selectedUser, dataFrame)
        if (mostCommon.shape[0] != 0):
            st.header("Top Words Used🥇")
        
            col1, col2 = st.columns(2)
            with col1:
                fig, ax = plt.subplots()
                plt.ylabel('Message').set_color('yellow')
                plt.xlabel('Frequency').set_color('yellow')
                ax.barh(mostCommon['Message'], mostCommon['Frequency'])
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            
            with col2:
                st.dataframe(mostCommon)
            
        # emoji analysis
        emoji_df = helper.mostEmoji(selectedUser, dataFrame)
        if (emoji_df.shape[0]!=0):
            st.title("Emoji Analysis😳")

            col1,col2 = st.columns(2)

            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig,ax = plt.subplots()
                color =  ['#FFC107', '#2196F3', '#4CAF50', '#F44336', '#9C27B0']

                ax.pie(emoji_df['Count'].head(),labels=emoji_df['Emoji'].head(),autopct="%0.2f", colors=color)
                ax.set_title("Emoji Distribution", color='yellow')
                fig.set_facecolor('#121212')
                st.pyplot(fig)