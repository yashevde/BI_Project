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

working_dir = './user_logs'

users = []
for root, dirs, _ in os.walk(working_dir):
    for d in dirs:
        if d.startswith('user-'):
            users.append(d)
users = sorted(users, key=lambda item: int(item.partition('-')[2]))

n_devices = []
n_calls = []
n_texts = []
n_contacts = []

total_talkTime = []
avg_talkTime = []
call_activity = []

text_activity = []

transaction_success = []

# mpesa_min = []
mpesa_max = []
mpesa_avg = []
mpesa_limit = []

# mshwari_min = []
mshwari_max = []
mshwari_avg = []

n_mshwari_loans = []
avg_mshwari_loan = []
max_mshwari_loan = []
# min_mshwari_loan = []
total_mshwari_loans = []

n_branch_loans = []
branch_loan_min = []
branch_loan_max = []
branch_loan_avg = []
branch_inst_avg = []

competition = []

n_expenditures = []
avg_expenditure = []
max_expenditure = []
min_expenditure = []
total_expenditure = []

n_incomes = []
avg_incoming = []
max_incoming = []
min_incoming = []
total_income = []

burn_rate = []

for user in users:

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
            user_calls = pd.read_json(user_call_log)
        except OverflowError:
            pass

    n_user_calls = len(user_calls)
    n_calls.append(n_user_calls)

    n_devices.append(len(user_call_logs))

    talkTime = (user_calls['duration'].sum())

    if n_user_calls != 0:
        total_talkTime.append(round((talkTime / 3600), 2))
        avg_talkTime.append((round((talkTime / 60), 2)) / n_user_calls)
    else:
        total_talkTime.append(0)
        avg_talkTime.append(0)

    # d/n ratio
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
        if 8 <= hr <= 23:
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
    texts_list = user_texts['message_body'].tolist()
    texts_list = ''.join(texts_list).lower()

    user_mpesa_bal = [re.findall(r'm-pesa balance is ksh(\d+)', texts_list)]
    user_mpesa_bal = list(map(int, list(itertools.chain.from_iterable(list(filter(None, user_mpesa_bal))))))

    if user_mpesa_bal:
        # mpesa_min.append(min(user_mpesa_bal))
        mpesa_max.append(max(user_mpesa_bal))
        mpesa_avg.append(np.mean(user_mpesa_bal))
    else:
        # mpesa_min.append(0)
        mpesa_max.append(0)
        mpesa_avg.append(0)

    user_mshwari_bal = [re.findall(r'm-shwari account balance is ksh(\d+)', texts_list)]
    user_mshwari_bal = list(map(int, list(itertools.chain.from_iterable(list(filter(None, user_mshwari_bal))))))

    if user_mshwari_bal:
        # mshwari_min.append(min(user_mshwari_bal))
        mshwari_max.append(max(user_mshwari_bal))
        mshwari_avg.append(round((np.mean(user_mshwari_bal)), 2))

    else:
        # mshwari_min.append(0)
        mshwari_max.append(0)
        mshwari_avg.append(0)

    user_mpesa_limit = [re.findall(r'your loan limit is (\d+)', texts_list)]
    user_mpesa_limit = list(map(int, list(itertools.chain.from_iterable(list(filter(None, user_mpesa_limit))))))

    if user_mpesa_limit:
        mpesa_limit.append(max(user_mpesa_limit))
    else:
        mpesa_limit.append(0)

    branch_loan_amt = [re.findall(r'branch loan of ksh (\d+)', texts_list)]
    branch_loan_amt = list(map(int, list(itertools.chain.from_iterable(list(filter(None, branch_loan_amt))))))

    n_branch = len(branch_loan_amt)

    if branch_loan_amt:
        n_branch_loans.append(n_branch)
        branch_loan_min.append(min(branch_loan_amt))
        branch_loan_max.append(max(branch_loan_amt))
        branch_loan_avg.append(round((np.mean(branch_loan_amt)), 2))
    else:
        n_branch_loans.append(0)
        branch_loan_min.append(0)
        branch_loan_max.append(0)
        branch_loan_avg.append(0)

    expenditures = [re.findall(r'confirmed. ksh(\d+)', texts_list), re.findall(r'give ksh(\d+)', texts_list)]
    expenditures = list(map(int, list(itertools.chain.from_iterable(list(filter(None, expenditures))))))

    sum_expenditure = sum(expenditures)

    if expenditures:
        n_expenditures.append(len(expenditures))
        avg_expenditure.append(np.mean(expenditures))
        max_expenditure.append(max(expenditures))
        min_expenditure.append(min(expenditures))
        total_expenditure.append(sum_expenditure)

    else:
        n_expenditures.append(0)
        avg_expenditure.append(0)
        max_expenditure.append(0)
        min_expenditure.append(0)
        total_expenditure.append(0)

    income_amts = [re.findall(r'you have received ksh(\d+)', texts_list)]
    income_amts = list(map(int, list(itertools.chain.from_iterable(list(filter(None, income_amts))))))

    sum_income = sum(income_amts)

    if income_amts:
        n_incomes.append(len(income_amts))
        avg_incoming.append(np.mean(income_amts))
        max_incoming.append(max(income_amts))
        min_incoming.append(min(income_amts))
        total_income.append(sum_income)

    else:
        n_incomes.append(0)
        avg_incoming.append(0)
        max_incoming.append(0)
        min_incoming.append(0)
        total_income.append(0)

    mshwari_loans_due = [re.findall(r'loan of ksh(\d+)', texts_list)]
    mshwari_loans_due = list(map(int, list(itertools.chain.from_iterable(list(filter(None, mshwari_loans_due))))))

    n_mshwari = len(mshwari_loans_due)

    if mshwari_loans_due:
        n_mshwari_loans.append(n_mshwari)
        avg_mshwari_loan.append(np.mean(mshwari_loans_due))
        max_mshwari_loan.append(max(mshwari_loans_due))
        total_mshwari_loans.append(sum(mshwari_loans_due))

    else:
        n_mshwari_loans.append(0)
        avg_mshwari_loan.append(0)
        max_mshwari_loan.append(0)
        total_mshwari_loans.append(0)

    if n_branch != 0:
        competition.append(n_mshwari / n_branch)
    else:
        competition.append(1)

    branch_installment = [re.findall(r'branch repayment of ksh (\d+)', texts_list)]
    branch_installment = list(map(int, list(itertools.chain.from_iterable(list(filter(None, branch_installment))))))

    if branch_installment:
        branch_inst_avg.append(round((np.mean(branch_installment)), 2))
    else:
        branch_inst_avg.append(0)

    counts.update(word.strip('.,?!"\'') for word in texts_list.split())
    confirmed = counts['confirmed'] + counts['confirmed.you']
    failed = counts['failed'] + counts['depleted'] + counts['finished.dial']
    if failed == 0:
        transaction_success.append(1)
    else:
        transaction_success.append((confirmed / (confirmed + failed)) * 100)

    if sum_income != 0 and sum_expenditure != 0:
        burn_rate.append(sum_expenditure / sum_income)
    if sum_income == 0 and sum_expenditure != 0:
        burn_rate.append(1)
    if (sum_income != 0 and sum_expenditure == 0) or (sum_income == 0 and sum_expenditure == 0):
        burn_rate.append(0)

    # d/n ratio
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
        if 8 <= hr <= 23:
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

    # TODO: degree assortativity -- use KNN?

feature_df = pd.DataFrame({'Total TalkTime (hrs)': total_talkTime, 'Average TalkTime (mins)': avg_talkTime,
                           '#Devices': n_devices, 'Day/Night Call ratio': call_activity,
                           'Day/Night Text ratio': text_activity, '#Contacts': n_contacts, '#Calls': n_calls,
                           '#Texts': n_texts,
                           '%Successful Transactions': transaction_success,
                           'Max MPESA Balance': mpesa_max, 'Avg MPESA Balance': mpesa_avg,
                           'Max MSHWARI Balance': mshwari_max, 'Avg MSHWARI Balance': mshwari_avg, '#MSHWARI Loans': n_mshwari_loans,
                           'Avg MSHWARI Loan': avg_mshwari_loan, 'Max MSHWARI Loan': max_mshwari_loan,
                           'Total MSHWARI Loans': total_mshwari_loans,
                           'MPESA Limit': mpesa_limit, '#Branch Loans': n_branch_loans,
                           'Min Branch Loan': branch_loan_min, 'Max Branch Loan': branch_loan_max, 'Avg Branch Loan': branch_loan_avg,
                           'Avg Branch Installment': branch_inst_avg, '#Expenditures': n_expenditures,
                           'Avg Expenditure': avg_expenditure, 'Max Expenditure': max_expenditure,
                           'Min Expenditure': min_expenditure, 'Total Expenditure': total_expenditure,
                           '#Incoming Amts': n_incomes, 'Competition': competition,
                           'Avg Incoming Amt': avg_incoming, 'Max Incoming Amt': max_incoming, 'Min Incoming Amt': min_incoming,
                           'Total Income': total_income, 'Burn Rate': burn_rate})

status = pd.read_csv('./user_logs_copy/user_status.csv', usecols=['status'])
status['status'] = status['status'].map({'repaid': 1, 'defaulted': 0})
df = pd.concat([feature_df, status], axis=1)

train, test = train_test_split(df, test_size=0.2)

print(df.head(5))

