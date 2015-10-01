#!/usr/bin/python 	
import time;
import cgi, cgitb
import os
from os import environ
import Cookie
import hashlib
from sql import *

ldb = sqldb()

cookie = Cookie.SimpleCookie()
cookie_string = os.environ.get('HTTP_COOKIE')
cookie.load(cookie_string)

if((not cookie_string) or ('hash' not in cookie) or ('email_id' not in cookie) or (not ldb.check_hash(cookie['hash'].value,cookie['email_id'].value))):
  print 'Content-type:text/html\r\n'+'Location: %s' % "logout.py"
  print "\r\n\r\n"

email_id = str(cookie['email_id']).split('=')[1]
if 'page' not in cookie.keys():
	cookie['page'] = '1'
	print cookie


form = cgi.FieldStorage()
#print form

if(form.getvalue('button')=='change password'):
	ldb.change_password(email_id,form.getvalue('para'))
	print 'Content-type:text/html\r\n'+'Location: %s' % "settings.py"
	print "\r\n\r\n"

if(form.getvalue('button')=='create folder'):
	ldb.create_folder(email_id,form.getvalue('para'))
	print 'Content-type:text/html\r\n'+'Location: %s' % "settings.py"
	print "\r\n\r\n"

if(form.getvalue('button')=='delete folder'):
	ldb.delete_folder(email_id,form.getvalue('para'))
	print 'Content-type:text/html\r\n'+'Location: %s' % "settings.py"
	print "\r\n\r\n"

d = dict()
d['from'] = 1
d['subject'] = 2
d['priority'] = 3
filter_obj = dict()

if(form.getvalue('button')=='Create Filter'):
	value = form.getvalue('para').split(':')
	filter_obj['email_id'] = email_id
	filter_obj['filter_type'] = d[value[0].lower()]
	filter_obj['action'] = 	value[1]
	filter_obj['filter_value'] = value[2]
	ldb.create_filter(filter_obj)
	print 'Content-type:text/html\r\n'+'Location: %s' % "settings.py"
	print "\r\n\r\n"

if(form.getvalue('button') == 'Delete Filter'):
	value = form.getvalue('para').split(':')
	filter_obj['email_id'] = email_id
	filter_obj['filter_type'] = d[value[0].lower()]
	filter_obj['filter_value'] = value[2]
	ldb.delete_filter(filter_obj)
	print 'Content-type:text/html\r\n'+'Location: %s' % "settings.py"
	print "\r\n\r\n"

print 'Content-type:text/html\r\n'+'Location: %s' % "settings.py"
print "\r\n\r\n"
