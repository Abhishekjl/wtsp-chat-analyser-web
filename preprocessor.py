import re
import pandas as pd
day_num = {
    'Monday':0,
    'Tuesday':1,
    'Wednesday':2,
    'Thursday':3,
    'Friday':4,
    'Saturday':5,
    'Sunday':6
}
def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s\w{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_message':messages,'message_date':dates})

    df['message_date'] = pd.to_datetime(df['message_date'],  format  = '%m/%d/%y, %I:%M %p - ')
    df.rename(columns = {'message_date':'date'}, inplace = True)
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2].lower())
        else:
            users.append('group_notifications')
            messages.append(entry[0])
    df['users'] = users
    df['messages'] = messages
    df.drop(columns = ['user_message'], inplace = True)
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['day_num'] = df['day_name'].map(day_num)
    df['only_date'] = df['date'].dt.date
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    return df