#!/usr/bin/python
import time;
import cgi, cgitb
import os
from os import environ
import Cookie
import hashlib
from sql import *
import binascii

print "Content-type: text/html"
print
localtime = time.asctime( time.localtime(time.time()) )
print "	Local current time :", localtime
print '</br>'
ldb = sqldb();


with open('menu.html') as f:
  print f.read()
cookie = Cookie.SimpleCookie()
cookie_string = os.environ.get('HTTP_COOKIE')
cookie.load(cookie_string)
email_id = str(cookie['email_id']).split('=')[1]
current_folder = str(cookie['folder']).split('=')[1]
folders = ldb.get_all_folder(email_id)
print '<ul>'
for row in folders :
		print '<ul><li><a href="inbox.py?folder='+row[0]+'">'+row[0]+'</a></li>'
print '</ul>'


unique = os.environ.get('QUERY_STRING')
unique_id = str(unique)[9:]

a = ldb.get_draft_from_id(unique_id)
#print a;


if(a[5]!=""):
	n = int(a[5], 2)
	data = binascii.unhexlify('%x' % n)
	f = open("/tmp/"+cookie['email_id'].value+".zip","wb")
	f.write(data)

print "<table>"
print "<tr><td><font size='3'><b>To</b></font></td><td></td><td>" + a[1] + '</td></tr>'
print "<tr><td><font size='3'><b>Priority </b></font></td><td></td><td>" + a[3] + '</td></tr>'


if(a[5]!=""):
	print '<tr><td><font size="3"><a href = "'+"/tmp/"+cookie['email_id'].value+".zip"+'" Download><font size="2.6"> Download Attachement</font></a></td><td></td><td></td></tr>' 

print "<tr><td><font size='3'><b>Subject </b></font></td><td></td><td>" + a[2] + '</td></tr>'


if(a[4]!=""):
	n = int(a[4],2)
	data = binascii.unhexlify('%x' % n)

	print "<tr><td><font size='3'><b>Body </b></font></td><td></td><td><textarea rows='10' cols='80' readonly>" + data + '</textarea></td></tr>'
else:
	print "<tr><td><font size='3'><b>Body </b></font></td><td></td><td>" + a[4] + '</td></tr>'
print "</table>"