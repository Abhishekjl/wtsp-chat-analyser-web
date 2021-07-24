from urlextract import URLExtract
from wordcloud import WordCloud
from wordcloud import STOPWORDS     
from collections import Counter
import emoji
import pandas as pd

stopwords = list(STOPWORDS) + ['omitted','media','will','<media','omitted>',]    


import numpy as np
extract = URLExtract()
def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    num_messages = df.shape[0]
    words = []
    for msg in df['messages']:
        words.extend([word for word in msg.split() if word not in stopwords])
    num_words = len(words)  

    # fetch number of media msgs
    num_media_messages =df[df['messages'] == '<media omitted>\n'].shape[0]
    # fetch number of links
    links = []
    for message in df.messages:
        links.extend(extract.find_urls(message))
    len_links = len(links)    
    return num_messages,num_words,num_media_messages, len_links

# fetch most active users
def most_active_users(df):
    x = df.users.value_counts().head()
    per_df = np.round((df.users.value_counts()/df.users.shape[0])*100,2).\
    reset_index().rename(columns = {'index':'User','users':'percentage'})
    return x,per_df

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df =  df[df['users'] == selected_user] 
    wc = WordCloud(stopwords = stopwords,width = 500, height = 500, min_font_size = 10)
    df_wc = wc.generate(df['messages'].str.cat(sep = " "))
    return df_wc    

def most_common_words(selected_user, df):
    words = []
    if selected_user != 'Overall':
        df =  df[df['users'] == selected_user]
    for msg in df['messages']:
        words.extend([word for word in msg.split() if word not in stopwords])


    most_common_words = pd.DataFrame(Counter(words).most_common(20), columns = ['words','frequency']).\
    sort_values(by= 'frequency')
    return most_common_words


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df =  df[df['users'] == selected_user]
    emojis = []
    for msg in df.messages:
        emojis.extend([c for c in msg if c in emoji.UNICODE_EMOJI['en']])    
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))), columns = ['emoji', '%used'])  
    emoji_df['%used'] = emoji_df['%used'].apply(lambda x:np.round((x/emoji_df.shape[0]),1))
    emoji_df = emoji_df.head(40)
    return emoji_df  

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df =  df[df['users'] == selected_user]
    timeline = df.groupby(['year','month_num','month']).count()['messages'].reset_index()   
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-'+ str(timeline['year'][i]))
    timeline['time'] = time
    return timeline    
def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df =  df[df['users'] == selected_user]
    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()
    return daily_timeline


def weekly_activity(selected_user, df):
    if selected_user != 'Overall':
        df =  df[df['users'] == selected_user]   
    return df.groupby(['day_name','day_num']).count()['messages'].reset_index().sort_values(by = 'day_num')
def monthly_activity(selected_user, df):
    if selected_user != 'Overall':
        df =  df[df['users'] == selected_user]  
    return df.groupby(['month', 'month_num']).count()['messages'].reset_index().sort_values(by = 'month_num')

def status_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df =  df[df['users'] == selected_user] 
    period_df = df.groupby(['hour','day_name','day_num']).count()['messages'].reset_index().sort_values(by = ['hour','day_num'])
    pivot = period_df.pivot('hour', 'day_name', 'messages').fillna(0)
    pivot = pivot[['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']].T
    return pivot
     


