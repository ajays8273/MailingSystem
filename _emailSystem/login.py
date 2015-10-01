#!/usr/bin/python
import cgi, cgitb
from sql import *
import os
import Cookie
import hashlib
import datetime
import time

form = cgi.FieldStorage()
email_id = form.getvalue('username')
psswd = form.getvalue('password')


ldb = sqldb()
if((not email_id) or (not psswd) or ldb.check_user(email_id,psswd)==False):
  print 'Content-type:text/html\r\n'+'Location: %s' % "/_emailSystem/"
  print "\r\n\r\n";

hashObj = hashlib.md5()
hashObj.update(email_id+psswd)

cookie = Cookie.SimpleCookie()
cookie['email_id'] = email_id
cookie['hash'] = hashObj.hexdigest()
cookie['folder'] = 'inbox'
cookie['page'] = '1'

print cookie



print 'Content-type:text/html\r\nLocation: %s' % "inbox.py"

print "\r\n\r\n"
