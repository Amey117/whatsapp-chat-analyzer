import pandas as pd
from urlextract import URLExtract
from collections import Counter
import emoji
import re

def data_analysis(user,df):
    if user=="Overall":
        return df.shape[0]
    else:
        g = df.groupby("User")
        return g.get_group(user).shape[0]

def count_words(user,df):
    if user=="Overall":
        words = []
        for message in df["Message"]:
            words.extend(message.split(" "))
        return len(words)
    else:
        words=[]
        for message in df[df["User"]==user]["Message"]:
            words.extend(message.split(" "))
        return len(words)

def media_count(user,df):
    if user!="Overall":
        g = df.groupby("User")
        df=g.get_group(user)
    return df[df["Message"] == "<Media omitted>\n"].shape[0]

def url_count(user,df):
    urls=[]
    extractor = URLExtract()
    if user!="Overall":
        g = df.groupby("User")
        df=g.get_group(user)
    for message in df["Message"]:
        urls.extend(extractor.find_urls(message))
    return len(urls)

def most_busyusers(df):
    x=df["User"].value_counts()
    return x
def most_used_words(df,selected_user):

    if selected_user!="Overall":
        df=df[df["User"]==selected_user]

    temp = df[(df["User"] != "Notification") & (df["Message"] != "<Media omitted>\n")]
    words = []
    f = open("stop_hinglish.txt", "r")
    stop_words = f.read()

    for msg in temp["Message"]:
        for word in msg.lower().split():
            if word not in stop_words:
                if word[0] != '@':
                    words.append(word)



    new_df=pd.DataFrame(Counter(words).most_common(20))

    return new_df


def emojis(df,selected_user):
    emojis=[]
    if selected_user!="Overall":
        df=df[df["User"]==selected_user]
    from collections import Counter
    for message in df["Message"]:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
    # pd.DataFrame(Counter(emojis))
    df = pd.DataFrame.from_dict(Counter(emojis), orient='index')
    df=df.reset_index()
    return df

def time_se(df):
    time_fr = df.groupby(["year","Month"]).count()["Message"].reset_index()
    timeline = []
    for i in range(time_fr.shape[0]):
        timeline.append(time_fr["Month"][i] + "-" + str(time_fr["year"][i]))
    #time_fr["time"] = timeline
    return time_fr

def day_analysis(df,selected_user):
    cats = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    if selected_user!="Overall":
        df=df[df["User"]==selected_user]
    return df["Day"].value_counts().reindex(cats).reset_index()

def month_analysis(df,selected_user):
    if selected_user!="Overall":
        df=df[df["User"]==selected_user]
    return pd.DataFrame(df["Month"].value_counts()).reset_index().sort_values(by="Month",ascending=False)

def daily_timeline(df,selected_user):
    if selected_user!="Overall":
        df=df[df["User"]==selected_user]
    return df.groupby("date").count()["Message"].reset_index()

def heat_map(df,selected_user):
    if selected_user!="Overall":
        df=df[df["User"]==selected_user]
    df['only_time'] = pd.to_datetime(df['Time'], format='%I:%M %p').dt.strftime('%H:%M:%S')
    df['new_only_time'] = pd.to_datetime(df['only_time'])
    hours = []
    for i in range(df.shape[0]):
        hours.append(df["new_only_time"][i].hour)
    df["hours"] = hours
    print(hours)
    period = []
    for hour in df['hours']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] = period
    user_heatmap = df.pivot_table(index='Day', columns='period', values='Message', aggfunc='count').fillna(0)
    return user_heatmap