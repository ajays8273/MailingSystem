#!/usr/bin/python
import cgi, cgitb
from sql import *
import os
import Cookie
import hashlib

form = cgi.FieldStorage()
username = form.getvalue('username')
password = form.getvalue('password')
email_id = form.getvalue('email-id')
university = form.getvalue('University')
dob = form.getvalue('dob')

db_obj = sqldb()

if(db_obj.find_user(email_id)==False):
	print 'Content-type:text/html\r\n\r\n'
	print '<script type="text/javascript">window.alert("email-id already present, Please register Again!!"); window.location.assign("/_emailSystem/");</script>'

db_obj.add_user(email_id,password,username,university,dob);

print 'Content-type:text/html\r\n\r\n'
print '<script type="text/javascript">window.alert("You are successfully registered, Please login again to open you mailbox"); window.location.assign("/_emailSystem/");</script>'