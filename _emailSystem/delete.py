#!/usr/bin/python
import time;
import cgi, cgitb
import os
from os import environ
import Cookie
import hashlib
from sql import *


ldb = sqldb();
unique = os.environ.get('QUERY_STRING')
unique_id = str(unique)[5:]
#print unique_id
values =  str(unique_id).split('@');
#print values
to = values[0]
from_ = values[1]
time  = values[2]
time = time.replace('%20',' ')
#print to , from_ , time
ldb.change_folder_email(to, from_, time, "r" , "delete")
print 'Content-type:text/html\r\n'+'Location: %s' % "inbox.py"	
print "\r\n\r\n"