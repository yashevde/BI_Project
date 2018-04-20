# BI_Project
## Yash Shevde
Instructions and Q&A:
https://docs.google.com/document/d/1XgYfGj73pXdhoB0L45cvg357wp81NWqs8fMscOchQCg/edit

## Insights and thought process:
Data Structure:
* user_status.csv
* user-n
    * device-n
        * collated_call_log.txt
        * collated_contact_list.txt
        * collated_sms_log.txt

Observations:
* contact names "cached_name" are idiosyncratic. phone number is primary ID marker in collated_call_log.txt

Hypotheses:

* potential correlated variables:
    * number of 'transactional' texts
    * number of devices
    * number of contacts
    * total number of phone calls made 
    (indicates high (talk-time balance)|(tier of phone plan))

Steps:
- [] build up Dataframe. merge logs across devices (+count); index by user.
- [] only keep useful sms rows from collated_sms_log.txt (sms_address==MPESA,Safaricom, branch). 
Basically, just non-numerical sms. Only recognized senders are labeled and pertinent.

## Active time log:
this will be useful in case I close the google doc while working on it, or keeping it open while not.
All times in P.T.

total: 

* 04/20 06:00 - 

Just realized that I've never had to crawl through subdirectories to build up the data. 

* 04/19 13:30 - 13:50

setup, examining data files, establishing some workflow
