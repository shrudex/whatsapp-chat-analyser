import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import emoji
import seaborn as sns
import plotly.express as px


st.set_page_config(page_title="Shrudex", layout="wide")

st.title("WhatsChat🔎")
st.write("*Made with❤️‍🔥 by Shrudex!👨🏻‍💻*")

st.sidebar.title("WhatsApp Chat Analyzer")
uploadedFile = st.sidebar.file_uploader("Choose a File🗃️")
if uploadedFile is not None:
    bytesData = uploadedFile.getvalue()
    finalData = bytesData.decode("utf-8")
    dataFrame = preprocessor.preprocess(finalData)
    #st.title("WhatsApp Chat Data")
    #st.dataframe(dataFrame.head())

    # fetch unique users
    userList = dataFrame["user"].unique().tolist()
    if ("default" in userList):
        userList.remove("default")
    userList.sort()
    userList.insert(0, "Overall")
    selectedUser = st.sidebar.selectbox("Show Analysis🤔 WRT", userList)

    #if st.sidebar.button("Show Analysis🔢"):
    if (True):
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

        # monthly timeline
        st.title("Monthly Timeline⌚")
        timeline = helper.monthlyTimeline(selectedUser, dataFrame)
        plt.style.use('dark_background')
        plt.figure(figsize=(12, 3))
        plt.plot(timeline['time'], timeline['message'])
        plt.xticks(rotation='vertical')
        plt.title(f"{selectedUser}", color='yellow')
        st.pyplot(plt)

        # daily timeline
        st.title("Daily Timeline📅")
        dailyTimeline = helper.dailyTimeline(selectedUser, dataFrame)
        plt.style.use('dark_background')
        plt.figure(figsize=(14, 3))
        plt.plot(dailyTimeline['onlyDate'], dailyTimeline['message'])
        plt.xticks(rotation='vertical')
        plt.title('Daily Message Count', color='yellow')
        plt.xlabel('Date', color='white')
        plt.ylabel('Message Count', color='white')
        st.pyplot(plt)

        # activity map
        st.title("Week Activity📊")
        col1, col2 = st.columns(2)
        weekActivitySeries, weekActivity = helper.weekActivity(selectedUser, dataFrame)
        weekActivity = weekActivity.sort_values('message')
        days = weekActivity['dayName']
        messages = weekActivity['message']
        
        with col2:
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.pie(messages, labels=days, autopct='%1.1f%%', colors=plt.cm.Dark2.colors)
            ax.axis('equal')
            plt.style.use('dark_background')
            st.pyplot(fig)
            
            
        with col1:
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.bar(days, messages)
            ax.set_xlabel('Day of the Week', color="yellow")
            ax.set_ylabel('Number of Messages', color='yellow')
            plt.style.use('dark_background')
            st.pyplot(fig)
        
        #------------------------------
        
        st.title("Month Activity📊")
        col1, col2 = st.columns(2)
        monthActivitySeries, monthActivity = helper.monthActivity(selectedUser, dataFrame)
        monthActivity = monthActivity.sort_values('message')
        month = monthActivity['monthName']
        messages = monthActivity['message']
        
        with col2:
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.pie(messages, labels=month, autopct='%1.1f%%', colors=plt.cm.Dark2.colors)
            ax.axis('equal')
            plt.style.use('dark_background')
            st.pyplot(fig)
            
            
        with col1:
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.bar(month, messages)
            ax.set_xlabel('Month of the Year', color="yellow")
            ax.set_ylabel('Number of Messages', color='yellow')
            plt.style.use('dark_background')
            st.pyplot(fig)
            
        #hourly activity
        st.title("Hour Activity⌛")
        h1, h2 = helper.hourActivity(selectedUser, dataFrame)
        
        fig, ax = plt.subplots(figsize=(12, 3))
        h1.unstack('dayName').plot(ax=ax)
        ax.set_xlabel('Hour of the Day', color='yellow')
        ax.set_ylabel('Number of Messages', color='yellow')
        ax.set_title('Messages Sent by Hour of the Day', color='white')
        plt.style.use('dark_background')
        st.pyplot(fig)
        
        #----
        st.header("Day-wise Activity🗓️")
        tabs = st.multiselect("Select day(s) to display",['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
        #tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        for day in tabs:
            day_data = h2[h2['dayName'] == day]
            plot_placeholder = st.empty()
            with plot_placeholder:
                fig, axs = plt.subplots(figsize=(12, 3))
                axs.plot(day_data['hour'], day_data['message'])
                axs.set_title(day)
                axs.set_xlabel('Hour of the Day', color='yellow')
                axs.set_ylabel('Number of Messages', color='yellow')
                axs.set_xticks(range(0, 24, 2))
                axs.grid(True, alpha=0.3)
                plt.tight_layout()
                st.pyplot(fig)
                
        #period activity
        st.header("Activity by Time Period📲")
        activity = helper.activity(selectedUser, dataFrame)
        activity = activity.sort_values('message')
        period = activity['period']
        messages = activity['message']
        fig, ax = plt.subplots(figsize=(16, 3))
        ax.bar(period, messages)
        ax.set_xlabel('Period', color="yellow")
        ax.set_ylabel('Number of Messages', color='yellow')
        ax.set_title('Activity Chart')
        plt.style.use('dark_background')
        st.pyplot(fig)



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
        if (emoji_df.shape[0] != 0):
            st.title("Emoji Analysis😳")

            col1, col2 = st.columns(2)

            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig, ax = plt.subplots()
                color = ['#FFC107', '#2196F3', '#4CAF50', '#F44336', '#9C27B0']

                ax.pie(emoji_df['Count'].head(), labels=emoji_df['Emoji'].head(
                ), autopct="%0.2f", colors=color)
                ax.set_title("Emoji Distribution", color='yellow')
                fig.set_facecolor('#121212')
                st.pyplot(fig)
        
        #message extractor
        st.title("Messages Extractor🪓")
        inputDate = st.text_input("Enter date in format : 19-08-2003")
        messageExtract = helper.messageExtractor(selectedUser, dataFrame, inputDate)
        if st.button("Extract"):
            if messageExtract.shape[0]>0:
                st.dataframe(messageExtract, width=1400)
            else:
                st.write("No conversation(s) on", inputDate)  

        #reply time analysis
        st.header("Reply Time Analysis⏩")
        timeDifference, timeSelected = helper.replyTime(selectedUser, dataFrame)
        if (selectedUser!='Overall'):
            st.write("Average Reply Time by", selectedUser, "is", timeSelected)
        else:
            col1, col2 = st.columns(2)
            with col1:
                fig, ax = plt.subplots(figsize=(8, 6))
                ax.bar(timeDifference['user'], timeDifference['replyTime'].dt.seconds)
                ax.set_xlabel('Participant', color='yellow')
                ax.set_ylabel('Average Reply Time (Seconds)', color='yellow')
                ax.set_title('')
                st.pyplot(plt)
            with col2:
                fig, ax = plt.subplots(figsize=(8, 6))
                ax.pie(timeDifference['replyTime'], labels=timeDifference['user'], autopct='%1.1f%%', colors=plt.cm.Dark2.colors)
                ax.axis('equal')
                plt.style.use('dark_background')
                ax.set_title('')
                st.pyplot(fig)
