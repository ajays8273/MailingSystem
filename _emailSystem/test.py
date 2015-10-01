from sql import *
import datetime
import time
import warnings
warnings.filterwarnings("ignore")

email_obj = dict()

email_obj['sender_email'] = 'parag'
email_obj['reciever_email'] = 'shri3011994'
email_obj['subject'] = 'testing'
email_obj['attachement'] = ''
email_obj['priority'] = 'high'
email_obj['time_stamp'] = str(datetime.datetime.now().replace(microsecond=0))
email_obj['flag'] = 1
email_obj['sender_folder'] = 'sent'
email_obj['receiver_folder'] = 'inbox'
email_obj['mail_body'] = 'Nothing Dude'

db = sqldb()

i=0
while(i<=30):
	time.sleep(0.5)
	email_obj['time_stamp'] = str(datetime.datetime.now().replace(microsecond=0))
	db.send_email(email_obj)





filter_obj = dict()

filter_obj['email_id']='shri3011994' 
filter_obj['filter_type']=1
filter_obj['action']='{delete}'
filter_obj['filter_value']='shaswata'

sd_obj = dict()

sd_obj['sender_email'] = email_obj['sender_email']
sd_obj['receiver_email'] = email_obj['reciever_email']
sd_obj['subject']=email_obj['subject']
sd_obj['priority']=email_obj['priority']
sd_obj['mail_body']=email_obj['mail_body']
sd_obj['attachement']=email_obj['attachement']
sd_obj['schedule_time']=email_obj['time_stamp']


# db.get_emails('shri3011994','sent',1,10,"s")
#print db.get_smail('shri3011994','parag', '2014-06-03 14:05:05')
