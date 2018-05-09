# BI_Project
## Yash Shevde
Instructions and Q&A:
https://docs.google.com/document/d/1XgYfGj73pXdhoB0L45cvg357wp81NWqs8fMscOchQCg/edit

## **Steps:**
- [x] import csv and txts into pd.Dataframe. merge across devices (and count them per user); index by user.
- [x] feature engineering from parameters
- [x] Datetime handling for call and sms logs
- [x] make master df. Split 80-20 into train and test.
- [-] Parse out info from texts -- expand.
- [] build and compare models, draw inferences
- [] start to tell the story of the data
- [] optimize BI_df.py
- [~] degree assortativity for network

## Active time log:
this will be useful in case I close the google doc while working on it, or keep it open while not.
All times in P.T.

**in progress**

* 05/09 15:00 - 16:00

regex text parsing, expanding feature space

noticed major bug in user call concatenation. Fixing.

* 05/08 14:00 - 15:00

text parsing, transaction success, some plots and correlation viz, train/test split

started prototyping for modeling with a basic skeleton for regression

* 05/07 16:00-17:00

error handling, talktime, call activity, n_contacts
resolving issues in assembling text for parsing: https://stackoverflow.com/a/46721064/8259724

beginning final df assembly

* 05/06 14:00 - 15:00

resuming work after delay (again, apologies for the lack of update during bike-accident recuperation)

took unlogged 20 mins to review understanding of data so far and where I was in the process

* 04/20 06:00 - 07:10

importing, exploring and cleaning data

* 04/19 13:30 - 13:50

setup, examining data files, establishing some workflow

## Insights and thought process:

* Correlations aren't too strong, which indicates good feature engineering. even and non-overlapping info content across the board.

**Surprises**

* branch features are quite strongly negatively correlated with status.
MPESA is a better financial feature so far.

**Hypotheses:**

* potential positively correlated variables to repayment:
    * number of 'transactional' texts (safaricom, mpesa, branch, mshwari)
        * safaricom: fewer "depleted", "almost finished"
        * M-PESA: : low(n_"failed"/n_"confirmed"), higher balance average ("account balance is")
        * M-Shwari: loan amount
        * Branch-co: fewer loans and lower "Your branch loan of" average
    * number of devices
    * number of contacts
    * total talk-time (collated_call_log.txt/"duration"--indicates high talk-time balance/tier of phone plan)
    * higher day/night ratio of number of outgoing calls/texts -- play around with bounds for day-time
    * higher n_times contacted for contacts with multiple phone numbers (== degree assortativity?)

## **Data Structure:**
* user_status.csv
* user-n
    * device-n
        * collated_call_log.txt
        * collated_contact_list.txt
        * collated_sms_log.txt

**Useful Parameters:**

* call logs:
    * duration
    * datetime
* sms log:
    * transactional messages number
    * transactional messages info
        * MPESA
        * M-Shwari
        * Safaricom
        * Branch-co
    * datetime
* contacts list:
    * n contacts
    * n phone numbers per contact
    * times contacted

