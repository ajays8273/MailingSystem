#!/usr/bin/python
import time;
import cgi, cgitb
import os
from os import environ
import Cookie
import hashlib
from sql import *



#print "hello"
form = cgi.FieldStorage()
values = form.getvalue('folder_move')


ldb = sqldb();
values =  str(values).split('@');
#print values
to = values[0]
from_ = values[1]
time  = values[2]
time = time.replace('%20',' ')
#print to , from_ , time , values[3]
ldb.change_folder_email(to, from_, time, "r" , values[3])
print 'Content-type:text/html\r\n'+'Location: %s' % "inbox.py"	
print "\r\n\r\n"