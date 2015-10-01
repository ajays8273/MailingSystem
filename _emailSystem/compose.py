#!/usr/bin/env python
#!/usr/bin/python
import cgi, cgitb 
from sql import *
import os
import Cookie
import hashlib
import time;
from os import environ
import datetime
import binascii
#print 'Content-type:text/html\r\n'
#print '\r\n\r\n'


try: 
    import msvcrt
    msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
    msvcrt.setmode (1, os.O_BINARY) # stdout = 1    
except ImportError:
    pass

ldb = sqldb()

cookie = Cookie.SimpleCookie()
cookie_string = os.environ.get('HTTP_COOKIE')
cookie.load(cookie_string)

if((not cookie_string) or ('hash' not in cookie) or ('email_id' not in cookie) or (not ldb.check_hash(cookie['hash'].value,cookie['email_id'].value))):
	print 'Content-type:text/html\r\n'+'Location: %s' % "logout.py"
	print "\r\n\r\n"

    
  

email_id = str(cookie['email_id']).split('=')[1]    
form = cgi.FieldStorage() 
rec_mail= form.getvalue('rec_email')
subj=form.getvalue('subject')
message=form.getvalue('message')
message=message.lstrip()
if(message == ""):
	message = "{Empty}"
message =  bin(int(binascii.hexlify(message), 16))
prior=form.getvalue('Prior')

value=form.getvalue('Send')
value2=form.getvalue('Save_Draft')
value3=form.getvalue('schedule_draft')
date = form.getvalue('date2')
date = date + ":00"

if(value=="Send"):
	
	#unique2 = os.environ.get('QUERY_STRING')
	#if(unique):
		#unique_id = str(unique)[9:]
		#current_folder = unique_id


	email_obj = dict()



	#print """\
	#Content-Type: text/html\n
	#<html><body>
	#"""  
	#print form['file']  

	if form.getvalue('file')!= "":
	
		fileitem = form['file']
	
	
	
		thedata = (fileitem.file.read())
		s =  bin(int(binascii.hexlify(thedata), 16))

		email_obj['reciever_email'] = rec_mail
	
		email_obj['subject'] = subj
		email_obj['mail_body'] = message
	
		email_obj['attachement']=s
		email_obj['sender_email']=email_id
		email_obj['sender_folder']="sent"
		email_obj['priority']=prior
		email_obj['flag']=0
	
		email_obj['time_stamp']=  str(datetime.datetime.now().replace(microsecond=0))
	
		email_obj['receiver_folder']=ldb.get_filter_action(email_id, rec_mail, subj, prior)
		ldb.send_email(email_obj)
	else:
		email_obj['reciever_email'] = rec_mail
		email_obj['subject'] = subj
		email_obj['mail_body'] = message
		email_obj['sender_email']=email_id
		email_obj['attachement']=""
		email_obj['sender_folder']="sent"
		email_obj['priority']=prior
		email_obj['flag']=0
		email_obj['time_stamp']=str(datetime.datetime.now().replace(microsecond=0))
		email_obj['receiver_folder']=ldb.get_filter_action(email_id, rec_mail, subj, prior)
	
		ldb.send_email(email_obj)
	print 'Content-type:text/html\r\n'+'Location: %s' % "inbox.py"
	print "\r\n\r\n"
if(value2=="Save_Draft"):

	sd_obj= dict()
	if form.getvalue('file')!= "":
	
		fileitem = form['file']
		thedata = (fileitem.file.read())
		s =  bin(int(binascii.hexlify(thedata), 16))
		sd_obj['sender_email']=email_id
		sd_obj['receiver_email']=rec_mail
		sd_obj['subject']=subj
		sd_obj['priority']=prior
		sd_obj['mail_body']=message
		sd_obj['attachement']=s
		ldb.save_draft(sd_obj)
		
	else:
		sd_obj['sender_email']=email_id
		sd_obj['receiver_email']=rec_mail
		sd_obj['subject']=subj
		sd_obj['priority']=prior
		sd_obj['mail_body']=message
		sd_obj['attachement']=""
		ldb.save_draft(sd_obj)
	
	print 'Content-type:text/html\r\n'+'Location: %s' % "draft.py"
	print "\r\n\r\n"
	#unique2 = os.environ.get('QUERY_STRING')
	#print unique
	#if(unique):
		#unique_id = str(unique)[9:]
		#current_folder = unique_id
		
if(value3=="schedule_draft"):

	sd_obj= dict()
	if form.getvalue('file')!= "":
	
		fileitem = form['file']
		thedata = (fileitem.file.read())
		s =  bin(int(binascii.hexlify(thedata), 16))
		sd_obj['sender_email']=email_id
		sd_obj['receiver_email']=rec_mail
		sd_obj['subject']=subj
		sd_obj['priority']=prior
		sd_obj['mail_body']=message
		sd_obj['attachement']=s
		sd_obj['schedule_time'] = date
		ldb.schedule_draft(sd_obj)
		
	else:
		sd_obj['sender_email']=email_id
		sd_obj['receiver_email']=rec_mail
		sd_obj['subject']=subj
		sd_obj['priority']=prior
		sd_obj['mail_body']=message
		sd_obj['attachement']=""
		sd_obj['schedule_time'] = date
		ldb.schedule_draft(sd_obj)
	
	print 'Content-type:text/html\r\n'+'Location: %s' % "schedule_draft.py"
	print "\r\n\r\n"
	#unique2 = os.environ.get('QUERY_STRING')
	#print unique
	#if(unique):
		#unique_id = str(unique)[9:]
		#current_folder = unique_id
		
