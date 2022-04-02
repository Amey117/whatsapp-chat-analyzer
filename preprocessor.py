import pandas as pd
import re


def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\sam\s-\s|\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\spm\s-\s'
    dates = re.findall(pattern, data)
    messages = re.split(pattern, data)[1:]
    df = pd.DataFrame({"user_message": messages, "Date": dates})
    user = []
    text = []
    notification = []
    pattern = "([\w\W]+?):\s"
    for item in df["user_message"]:
        entry = re.split(pattern, item)
        if len(entry) > 1:
            user.append(entry[1])
            text.append(entry[2])
        else:
            user.append("Notification")
            text.append(entry[0])
    df["User"] = user
    df["Message"] = text
    df.drop(columns=["user_message"], inplace=True)
    date = []
    time = []
    for item in df["Date"]:
        entry = item.split(",")
        time.append(entry[1].split("-")[0].strip())
        date.append(entry[0])

    df["date"] = date
    df["time"] = time
    df.drop(columns=["Date"], inplace=True)
    df.rename(columns={"date": "Date", "time": "Time"}, inplace=True)
    df = df.iloc[:, [2, 3, 0, 1]]
    df["date"] = pd.to_datetime(df['Date'])
    df.drop(columns=["Date"], inplace=True)
    df["Month"] = df['date'].dt.month_name()
    df["Day"] = df['date'].dt.day_name()
    df['Day_num'] = df['date'].dt.day
    df['Month_num'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df = df.iloc[:, [3, 6, 7, 8, 4, 5, 0, 1, 2]]
    return df

