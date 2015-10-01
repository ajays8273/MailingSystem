#!/usr/bin/python
import cgi, cgitb
import os
import Cookie
import hashlib
from sql import *

cookie = Cookie.SimpleCookie()
cookie_string = os.environ.get('HTTP_COOKIE')

if((not cookie_string)):
  print 'Content-type:text/html\r\n'+'Location: %s' % "/_emailSystem/"	
  print "\r\n\r\n"

cookie.load(cookie_string)
for d in cookie:
  cookie[d] = 'none'

print cookie

print 'Content-type:text/html\r\n'
print "\r\n\r\n"
print '<script type="text/javascript">\
		window.location.assign("/_emailSystem/");\
		</script>}'
