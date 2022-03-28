from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
from urlextract import URLExtract
extract=URLExtract()

def fetch_stats(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user] 
    number_of_messages=df.shape[0] 
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
    number_of_medias=df[df['message']=='<Media omitted>\n'].shape[0]
    links=[]
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return number_of_messages,len(emojis),number_of_medias,len(links)

def fetch_most_active_users(df):
    most_active_users_df=df['user'].value_counts().head(5)
    percentage_df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'User','user':'Percent'})
    return most_active_users_df,percentage_df

def create_wordcloud(selected_user,df):
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    temp=df[df['user']!='group_notification']
    temp=temp[temp['message']!='<Media omitted>\n']
    temp = temp[temp['message']!='This message was deleted\n']
    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)
    wc = WordCloud(height=450,width=500,min_font_size=10,background_color='white') 
    temp['message']=temp['message'].apply(remove_stop_words)
    wordcloud_image=wc.generate(temp['message'].str.cat(sep=' '))  
    return wordcloud_image

def most_used_emoji(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    emojis_list=[]
    for message in df['message']:
        emojis_list.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
    emoji_df=pd.DataFrame(Counter(emojis_list).most_common(10))
    emoji_df.rename(columns={0:'Emoji', 1:'Count'}, inplace=True)
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    month_timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(month_timeline.shape[0]):
        time.append(month_timeline['month'][i] + "-" + str(month_timeline['year'][i]))
    month_timeline['time'] = time
    return month_timeline

def daily_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    day_timeline = df.groupby('only_date').count()['message'].reset_index()
    return day_timeline

def week_activity_map(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    return df['day_name'].value_counts() 

def month_activity_map(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    return df['month'].value_counts() 