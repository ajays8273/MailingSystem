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
unique_id = str(unique)[9:]
#print unique_id
values =  str(unique_id).split('@');
#print values
from_ = values[0]
to = values[1]
time  = values[2]
time = time.replace('%20',' ')
#print to , from_ , time


ldb.delete_smail(from_,to,time)
print 'Content-type:text/html\r\n'+'Location: %s' % "schedule_draft.py"	
print "\r\n\r\n"