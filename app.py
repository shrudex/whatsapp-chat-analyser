import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import emoji
import seaborn as sns


st.set_page_config(page_title="Shrudex", layout="wide")

st.title("WhatsApp Chat Analyzer🔎")
st.write("Made with❤️‍🔥 by Shrudex!👨🏻‍💻")

st.sidebar.title("WhatsApp Chat Analyzer")
uploadedFile = st.sidebar.file_uploader("Choose a File🗃️")
if uploadedFile is not None:
    bytesData = uploadedFile.getvalue()
    finalData = bytesData.decode("utf-8")
    dataFrame = preprocessor.preprocess(finalData)
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

        # finding busiest users in the group
        if selectedUser == 'Overall':
            st.header("Top Chatters🗣️")
            topChatter, topChatterPercent = helper.mostBusy(dataFrame)
            col1, col2 = st.columns(2, gap='medium')

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
        st.header("Top Words Used🥇")
        mostCommon = helper.mostCommon(selectedUser, dataFrame)
        
        col1, col2 = st.columns(2, gap='medium')
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
        st.title("Emoji Analysis😳")

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)
