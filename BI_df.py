import numpy as np
import pandas as pd
import re
import os
import datetime
import warnings

working_dir = './user_logs_copy'

users = []
for root, dirs, _ in os.walk(working_dir):
    for d in dirs:
        if d.startswith('user-'):
            users.append(d)
users = sorted(users, key=lambda item: int(item.partition('-')[2]))

n_devices = []
talkTime = []
call_activity = []
n_contacts = []
# user 9 is a great reference. I user with >1 devices.
for user in users:
    n_devices.append(len(next(os.walk(working_dir + '/' + user))[1]))

    user_call_logs = []
    user_text_logs = []
    user_contact_logs = []
    for u, device, files in os.walk(working_dir + '/' + user):
        if not u.endswith(user):  # solution for device folder "u" repetition
            for filename in files:
                if filename.endswith('call_log.txt'):
                    user_call_logs.append(os.path.join(u, filename))
                if filename.endswith('sms_log.txt'):
                    user_text_logs.append(os.path.join(u, filename))
                if filename.endswith('list.txt'):
                    user_contact_logs.append(os.path.join(u, filename))

    for user_call_log in user_call_logs:
        try:
            user_calls = pd.read_json(user_call_log)  # ,date_unit='ms',keep_default_dates=True
        except OverflowError:
            pass

    # user talktime
    talkTime.append((user_calls['duration'].sum()) / 3600)

    # d/n ratio -- outgoing vs. incoming?
    d = 1
    n = 1
    for dt in user_calls['datetime']:
        dt = str(dt)
        for fmt in ('%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S'):
            try:
                DON = datetime.datetime.strptime(dt, fmt)
            except ValueError:
                pass
        hr = DON.hour
        if hr >= 8 and hr < 20:
            d += 1
        else:
            n += 1
    call_activity.append(round(d / n, 2))

    for user_text_log in user_text_logs:
        user_texts = pd.read_json(user_text_log)

    # parse
    # subset of df with just relevant rows
    # warnings.simplefilter(action='ignore', category=FutureWarning) -- next line is pain point
    # texts_df = user_texts[(user_texts.sms_address == 'MPESA') | (user_texts.sms_address == 'Branch-co') | (user_texts.sms_address == 'M-Shwari') | (user_texts.sms_address == 'Safaricom')]
    # texts_df = texts_df['message_body']

    # d/n ratio for texts as well?

    for user_contact_log in user_contact_logs:
        user_contacts = pd.read_json(user_contact_log)

    # n contacts
    n_contacts.append(len(user_contacts))
    # contact "richness"

    df = pd.DataFrame({'talkTime (hrs)': talkTime, 'n_devices': n_devices, 'call (day/night)': call_activity,
                       'n_contacts': n_contacts})

# print(df)

# master_df = concat user_dfs [user, repayed?, talktime, n_devices, n_contacts, d/n ratio, ...]
