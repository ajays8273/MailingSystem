#!/usr/bin/python
import time;
import cgi, cgitb
import os
from os import environ
import Cookie
import hashlib
from sql import *


cookie = Cookie.SimpleCookie()
cookie_string = os.environ.get('HTTP_COOKIE')

if((not cookie_string)):
  print 'Content-type:text/html\r\n'+'Location: %s' % "/_emailSystem/"	
  print "\r\n\r\n"

cookie.load(cookie_string)
unique = os.environ.get('QUERY_STRING')
 
data = unique.split('&')

cookie['page'] = data[0].split('=')[1]

print cookie

print 'Content-type:text/html\r\n\r\n'
print '<script type="text/javascript">window.location.assign("draft.py");</script>'
