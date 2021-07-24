import streamlit as st
import preprocessor
import matplotlib.pyplot as plt
import helper
import seaborn as sns
st.sidebar.title('Whatsapp chats analyzer')
uploaded_file = st.sidebar.file_uploader('Choose a wtsp_txt file')
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)

    # STATS AREA
    # fetch unique users
    user_list = df['users'].unique().tolist()
    try:
        user_list.remove('group_notifications')
    except:
        pass    
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox('Show analysis w.r.t',user_list)
    if st.sidebar.button("Show Analysis"):
        num_messages, num_words, num_media_msgs, num_links = helper.fetch_stats(selected_user, df)
        st.title('Top Statistic')
        col1,col2,col3,col4 = st.beta_columns(4)
        with col1:
            st.header('Total Msgs')
            st.title(num_messages)
        with col2:
            st.header('Total Words')
            st.title(num_words)
        with col3:
            st.header('Media Shared')
            st.title(num_media_msgs)   
        with col4:
            st.header('Link Shared')
            st.title(num_links)         
        # timeline
        st.title('Monthly Timeline')
        monthly_timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(monthly_timeline.time, monthly_timeline.messages)
        plt.xticks(rotation = 'vertical', color = 'black')
        st.pyplot(fig)       

        st.title('Daily Timeline')
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline.messages)
        plt.xticks(rotation = 'vertical', color = 'black')
        st.pyplot(fig)       

    # weekly time analysis
    st.title('Activity Map')
    col1, col2 = st.beta_columns(2)
    with col1:
        st.header('Most Busy Days')
        busy_day = helper.weekly_activity(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(busy_day.day_name,busy_day.messages, color = 'green')
        plt.xticks(rotation = 'vertical', color = 'black')

        st.pyplot(fig)
    with col2:
        st.header('Most busy month')
        busy_month = helper.monthly_activity(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(busy_month.month, busy_month.messages, color = 'orange')
        plt.xticks(rotation = 'vertical', color = 'black')
        st.pyplot(fig)    


    # GROUP STATISTICS
    if selected_user == 'Overall':
        st.title('Most Active Users')
        x,per_df = helper.most_active_users(df)
        fig, ax = plt.subplots()
        
        col1, col2 = st.beta_columns(2)
        with col1:
            ax.bar(x.index, x.values)
            plt.xticks(rotation = 'vertical', color = 'black')
            st.pyplot(fig)
        with col2:
            st.dataframe(per_df)

    # Wordcloud formation
    st.title('Word Cloud')
    df_wc = helper.create_wordcloud(selected_user,df)
    fig, ax = plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)
    
    # most common  words
    most_common_df = helper.most_common_words(selected_user,df)
    fig, ax = plt.subplots()
    ax.barh(most_common_df['words'], most_common_df['frequency'])
    plt.xticks(rotation = 'vertical')
    st.title('most common words')
    st.pyplot(fig)
    # heatmap 
    st.title('Online Status:')
    fig, ax = plt.subplots()
    pivot = helper.status_heatmap(selected_user, df)
    ax = sns.heatmap(pivot)
    st.pyplot(fig)


# emoji analyis 
    emoji_df = helper.emoji_helper(selected_user,df)
    st.title('emoji analyis')
    col1, col2 = st.beta_columns(2)
    with col1:
        st.dataframe(emoji_df)
    # with col2: