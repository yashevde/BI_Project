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
    * number of devices
    * number of contacts
    * total talk-time (collated_call_log.txt/"duration"--indicates high talk-time balance/tier of phone plan)
    
**Useful Parameters:**

* call logs:
    * duration
    * datetime
    * phone numbers -- cross-correlating with contacts?
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
- [] total duration of calls = sum (call_log//duration per user)
- [] Parse out info from (sms_address=="M-PESA","Safaricom", "Branch-co"). 
- [] Datetime handling for call and sms log to find day/night ratio of conversations

## Active time log:
this will be useful in case I close the google doc while working on it, or keeping it open while not.
All times in P.T.

**running total: 1.5hrs**

* 04/20 06:00 - 7:10

Just realized that I've never had to crawl through subdirectories to build up the data. 

* 04/19 13:30 - 13:50

setup, examining data files, establishing some workflow
