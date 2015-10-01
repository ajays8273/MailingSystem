from sql import *
import datetime
import warnings
import time
warnings.filterwarnings("ignore")

db_obj = sqldb()
i=0

while(1):
    time = str(datetime.datetime.now().replace(microsecond=0))
    to_send = db_obj.pick_schedule_draft(time)
    if(to_send):
        for emails in to_send:
            email_obj = dict()
            email_obj['sender_email'] = emails[0]
            email_obj['reciever_email'] = emails[1]
            email_obj['subject'] = emails[2]
            email_obj['attachement'] = emails[5]
            email_obj['priority'] = emails[3]
            email_obj['time_stamp'] = emails[6]
            email_obj['flag'] = 0
            email_obj['sender_folder'] = 'sent'
            folder = db_obj.get_filter_action(email_obj['sender_email'],email_obj['reciever_email'],email_obj['subject'],email_obj['priority'])
            #print email_obj['sender_email'],email_obj['reciever_email'],email_obj['subject'],email_obj['priority'],folder
            #print db_obj.get_filter(email_obj['reciever_email'])
            email_obj['receiver_folder'] = folder
            email_obj['mail_body'] = emails[4]
            db_obj.send_email(email_obj)
        db_obj.delete_schedule_draft(time)