import pandas as pd
from collections import Counter
from wordcloud import WordCloud
from turtle import back
from urlextract import URLExtract
import emoji
extractor = URLExtract()


def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # 1. fetch no. of messages
    num_messages = df.shape[0]

    # 2. number of words
    words = []
    for message in df['message']:
        words.extend(message.split())
    len_words = len(words)

    # 3. number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # 4. number of Link Shared
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))
    no_of_link = len(links)
    return num_messages, len_words, num_media_messages, no_of_link

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df['month'].value_counts()

def most_busy_users(df):
    X = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0]) * 100,
               2).reset_index().rename(columns={'index': 'name', 'user': 'percent'})
    return X, df


def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=10,
                   background_color='white')
    df = df[df['message'] != '<Media omitted>\n']
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    df_most_common = pd.DataFrame(Counter(words).most_common(20))
    return df_most_common


def emoji_counter(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(20))
    return emoji_df

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return heatmap