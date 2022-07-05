import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # st.dataframe(df)

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("show Analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages, len_words, num_media_messages, no_of_link = helper.fetch_stats(
            selected_user, df)
        st.title('Top Analysis Stats')
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("total Messages")
            st.title(num_messages)
        with col2:
            st.header("total Words")
            st.title(len_words)
        with col3:
            st.header("total medias")
            st.title(num_media_messages)
        with col4:
            st.header("total links shared")
            st.title(no_of_link)

        # Monthly TimeLine
        st.title('Monthly Timeline')
        timeline = helper.monthly_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color = 'orange')
        plt.xticks(rotation = 40)
        st.pyplot(fig)

        # Daily Timeline
        st.title('Daily Timeline')
        timeline = helper.daily_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(timeline['only_date'],timeline['message'], color = 'yellow')
        plt.xticks(rotation = 40)
        st.pyplot(fig)

        # Activity Map
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color = 'orange')
            plt.xticks(rotation = 40)
            st.pyplot(fig)
        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color = 'yellow')
            plt.xticks(rotation = 40)
            st.pyplot(fig)
        
        # Heatmap
        st.title('Activity Heatmap')
        heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(heatmap)
        st.pyplot(fig)

        # finding the busiest users in the group (group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            X, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)
            with col1:
                ax.bar(X.index, X.values)
                plt.xticks(rotation=30)
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.title('Word Cloud')
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common word
        st.title('most common Words')
        df_most_common = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(df_most_common[0], df_most_common[1], color='red')
        plt.xticks(rotation=30)
        st.pyplot(fig)

        # most Frequent Emojis
        st.title('Emoji Frequency')
        emoji_df = helper.emoji_counter(selected_user, df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.bar(emoji_df[0], emoji_df[1])
            st.pyplot(fig)
