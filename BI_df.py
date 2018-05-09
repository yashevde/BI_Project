import numpy as np
import pandas as pd
import re
import os
import datetime
import warnings
from collections import Counter
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import seaborn as sns
import itertools

counts = Counter()

working_dir = './user_logs_copy'

users = []
for root, dirs, _ in os.walk(working_dir):
    for d in dirs:
        if d.startswith('user-'):
            users.append(d)
users = sorted(users, key=lambda item: int(item.partition('-')[2]))

n_devices = []
total_talkTime = []
avg_talkTime = []
data_usage = []
call_activity = []
text_activity = []
n_calls = []
n_texts = []
n_contacts = []
transaction_success = []

mpesa_min = []
mpesa_max = []
mpesa_avg = []
mpesa_limit = []
mshwari_min = []
mshwari_max = []
mshwari_avg = []
branch_loan_min = []
branch_loan_max = []
branch_loan_avg = []

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
            user_calls = pd.read_json(user_call_log)  # ,date_unit='ms' ,keep_default_dates=True
        except OverflowError:
            pass
    n_user_calls = len(user_calls)
    n_calls.append(n_user_calls)

    # print(user, user_calls.head(5))
    talkTime = (user_calls['duration'].sum())

    if n_user_calls != 0:
        total_talkTime.append(round((talkTime / 3600), 2))
        avg_talkTime.append((round((talkTime / 60), 2)) / n_user_calls)
    else:
        total_talkTime = 0
        avg_talkTime = 0

    # d/n ratio TODO: outgoing vs. incoming?
    d = 0
    n = 0
    for dt in user_calls['datetime']:
        dt = str(dt)
        for fmt in ('%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S'):
            try:
                DON = datetime.datetime.strptime(dt, fmt)
            except ValueError:
                pass
        hr = DON.hour
        if 8 <= hr < 20:
            d += 1
        else:
            n += 1
    if n == 0:
        call_activity.append(1)
    else:
        call_activity.append(round(d / n, 2))

    for user_text_log in user_text_logs:
        user_texts = pd.read_json(user_text_log)
    n_texts.append(len(user_texts))

    # parse

    # subset of df with just relevant rows
    # warnings.simplefilter(action='ignore', category=FutureWarning) -- next line is pain point
    # try:
    # texts_df = user_texts[(user_texts.sms_address == 'MPESA') | (user_texts.sms_address == 'Branch-co') |
    # (user_texts.sms_address == 'M-Shwari') | (user_texts.sms_address == 'Safaricom')]
    # except FutureWarning:
    #    pass
    # texts_df = texts_df['message_body']
    # print(texts_df)
    # transactional_activity = len(texts_df)

    user_mshwari_trans = [] #
    mshwari_loans_due = [] #
    branch_installment = [] #
    income_amts = [] #
    expenditures = [] #

    texts_list = user_texts['message_body'].tolist()
    text_body = ''.join(texts_list).lower()
    # quickly scripted a word cloud to get the keywords to count

    user_mpesa_bal = [re.findall(r'm-pesa balance is ksh(\d+)', text_body)]
    user_mpesa_bal = list(filter(None, user_mpesa_bal))
    user_mpesa_bal = list(itertools.chain.from_iterable(user_mpesa_bal))
    user_mpesa_bal = list(map(int, user_mpesa_bal))

    if user_mpesa_bal:
        mpesa_min.append(min(user_mpesa_bal))
        mpesa_max.append(max(user_mpesa_bal))
        mpesa_avg.append(round((np.mean(user_mpesa_bal)), 2))
    else:
        mpesa_min.append(0)
        mpesa_max.append(0)
        mpesa_avg.append(0)

    user_mpesa_limit = [re.findall(r'your loan limit is (\d+)', text_body)]
    user_mpesa_limit = list(filter(None, user_mpesa_limit))
    user_mpesa_limit = list(itertools.chain.from_iterable(user_mpesa_limit))
    user_mpesa_limit = list(map(int, user_mpesa_limit))

    if user_mpesa_limit:
        mpesa_limit.append(max(user_mpesa_limit))
    else:
        mpesa_limit.append(0)

    user_mshwari_bal = [re.findall(r'm-shwari account balance is ksh(\d+)', text_body)]
    user_mshwari_bal = list(filter(None, user_mshwari_bal))
    user_mshwari_bal = list(itertools.chain.from_iterable(user_mshwari_bal))
    user_mshwari_bal = list(map(int, user_mshwari_bal))

    if user_mshwari_bal:
        mshwari_min.append(min(user_mshwari_bal))
        mshwari_max.append(max(user_mshwari_bal))
        mshwari_avg.append(round((np.mean(user_mshwari_bal)), 2))

    else:
        mshwari_min.append(0)
        mshwari_max.append(0)
        mshwari_avg.append(0)

    branch_loan_amt = [re.findall(r'branch loan of ksh (\d+)', text_body)]
    branch_loan_amt = list(filter(None, branch_loan_amt))
    branch_loan_amt = list(itertools.chain.from_iterable(branch_loan_amt))
    branch_loan_amt = list(map(int, branch_loan_amt))

    if branch_loan_amt:
        branch_loan_min.append(min(branch_loan_amt))
        branch_loan_max.append(max(branch_loan_amt))
        branch_loan_avg.append(round((np.mean(branch_loan_amt)), 2))
    else:
        branch_loan_min.append(0)
        branch_loan_max.append(0)
        branch_loan_avg.append(0)

    user_mshwari_trans.append(re.findall(r'you have transferred ksh(\d+)', text_body))
    mshwari_loans_due.append(re.findall(r'loan of ksh(\d+)', text_body))
    branch_installment.append(re.findall(r'branch repayment of ksh (\d+)', text_body))
    income_amts.append(re.findall(r'you have received ksh(\d+)', text_body))
    expenditures.append(re.findall('Confirmed. Ksh(\d+) paid', text_body))
    expenditures.append(re.findall('Confirmed. Ksh(\d+) sent', text_body))
    expenditures.append(re.findall('Give Ksh(\d+) cash', text_body))


    for text in texts_list:
        counts.update(word.strip('.,?!"\'').lower() for word in text.split())
    confirmed = counts['confirmed']+counts['confirmed.you']
    failed = counts['failed']+counts['depleted']+counts['finished.dial']
    if failed == 0:
        transaction_success.append(1)
    else:
        transaction_success.append((confirmed / (confirmed + failed)) * 100)

    # d/n ratio TODO: outgoing vs. incoming?
    d = 0
    n = 0
    for dt in user_texts['datetime']:
        dt = str(dt)
        for fmt in ('%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S'):
            try:
                DON = datetime.datetime.strptime(dt, fmt)
            except ValueError:
                pass
        hr = DON.hour
        if 8 <= hr < 20:
            d += 1
        else:
            n += 1
    if n == 0:
        text_activity.append(1)
    else:
        text_activity.append(round(d / n, 2))

    for user_contact_log in user_contact_logs:
        user_contacts = pd.read_json(user_contact_log)

    # n contacts
    n_contacts.append(len(user_contacts))

    # TODO: network "richness"

feature_df = pd.DataFrame({'total_talkTime_hrs': total_talkTime, 'avg_talkTime_mins': avg_talkTime,
                           'n_devices': n_devices, 'calls_d/n': call_activity,
                           'texts_d/n': text_activity, 'n_contacts': n_contacts, 'n_calls': n_calls, 'n_texts': n_texts,
                           'transaction_success': transaction_success, 'mpesa_min': mpesa_min,
                           'mpesa_max': mpesa_max, 'mpesa_avg': mpesa_avg, 'mshwari_min': mshwari_min,
                           'mshwari_max': mshwari_max, 'mshwari_avg': mshwari_avg, 'mpesa_limit': mpesa_limit,
                           'branch_min': branch_loan_min, 'branch_max': branch_loan_max, 'branch_avg': branch_loan_avg})

status = pd.read_csv('./user_logs_copy/user_status.csv', usecols=['status'])
status['status'] = status['status'].map({'repaid': 1, 'defaulted': 0})
df = pd.concat([feature_df, status], axis=1)

train, test = train_test_split(df, test_size=0.2)

# print(df)

# [degree assortativity, avg. loan amt]
# sentiment analysis?
