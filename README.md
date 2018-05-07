# BI_Project
## Yash Shevde
Instructions and Q&A:
https://docs.google.com/document/d/1XgYfGj73pXdhoB0L45cvg357wp81NWqs8fMscOchQCg/edit

## Observations and Inferences
* 

## Insights and thought process:
**Data Structure:**
* user_status.csv
* user-n
    * device-n
        * collated_call_log.txt
        * collated_contact_list.txt
        * collated_sms_log.txt

**Hypotheses:**

* potential positively correlated variables to repayment:
    * number of 'transactional' texts (safaricom, mpesa, branch)
        * safaricom: fewer "depleted", "almost finished"
        * M-PESA: high average balance
        * branch: fewer loans and amount per
    * number of devices
    * number of contacts
    * total talk-time (collated_call_log.txt/"duration"--indicates high talk-time balance/tier of phone plan)
    * higher day/night ratio of number of outgoing calls

**Useful Parameters:**

* call logs:
    * duration
    * datetime
    * country ISO
* sms log:
    * transactional messages number
    * transactional messages info
    * datetime
* contacts list:
    * n contacts
    * n phone numbers each contact possess
        * with number of times contacted factored in == degree of communication with a richer network?

**Steps:**
- [x] import csv and txts into pd.Dataframe. merge across devices (and count them per user); index by user.
- [x] total duration of calls = sum (call_log//duration per user)
- [] Parse out info from (sms_address=="M-PESA","Safaricom", "Branch-co"). 
- [] Datetime handling for call and sms log to find day/night ratio of conversations
- [] degree of communication parameter (number of calls to people with multiple lines i.e. more buying power/enterprise)
- [] make master df. Split 80-20 into train and test.

## Active time log:
this will be useful in case I close the google doc while working on it, or keep it open while not.
All times in P.T.

**running total: 2.5hrs**

* 05/06 14:00 - 15:00

resuming work after delay (again, apologies for the lack of update during bike-accident recuperation)
took unlogged 20 mins to review understanding of data so far and where I was in the process

* 04/20 06:00 - 07:10

importing, exploring and cleaning data

* 04/19 13:30 - 13:50

setup, examining data files, establishing some workflow
