import pandas as pd
import re
def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_messages': messages, 'date_time': dates})
    df['date_time'] = pd.to_datetime(df['date_time'], format='%d/%m/%Y, %H:%M - ')

    users = []
    messages = []
    for i in df['user_messages']:
        entry = re.split('([\w\W]+?):\s', i)
        if entry[1:]:
            users.append(entry[1])
            messages.append(''.join(entry[2]))
        else:
            users.append('grp_notification')
            messages.append(entry[0])
    df['users'] = users
    df['messages'] = messages
    df.drop(columns='user_messages', inplace=True)

    df['only_date'] = df['date_time'].dt.date
    df['year'] = df['date_time'].dt.year
    df['month_num'] = df['date_time'].dt.month
    df['month'] = df['date_time'].dt.month_name()
    df['day'] = df['date_time'].dt.day
    df['day_name'] = df['date_time'].dt.day_name()
    df['hour'] = df['date_time'].dt.hour
    df['minute'] = df['date_time'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df