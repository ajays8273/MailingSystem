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
  


#print str(cookie['email_id']).split('=')[1]

email_id = str(cookie['email_id']).split('=')[1]
if 'page' not in cookie.keys():
	cookie['page'] = '1'
	print cookie


print "Content-type: text/html"
print 
print "hello "


localtime = time.asctime( time.localtime(time.time()) )
print "	Local current time :", localtime
print '</br>'

with open('menu.html') as f:
  print f.read()

#print environ

current_folder = "settings"	

folders = ldb.get_all_folder(email_id)
print '<ul>'
for row in folders :
		print '<ul><li><a href="inbox.py?folder='+row[0]+'" onclick= '+"'delete_cookies()'"+' >'+row[0]+'</a></li>'
print '</ul>'
print '</br>'

unique = os.environ.get('QUERY_STRING')
if(unique):
	unique_id = str(unique)[7:]
	current_folder = unique_id
print "</br>"
print "</br>"

print "</br>"

print "</br>"

print "<table align='center'><tbody>"

print "	<form action='settings_back.py' onSubmit='return finalcheck(1);'>\
			<tr>\
			<td>New Password</td><td><input type = 'text' name='para'  id = '1'></td>\
			<td><input type='submit' name= 'button'  value='change password'></td>\
			</tr>\
		</form>"

print "	<form action='settings_back.py' onSubmit='return finalcheck(2);'>\
			<tr>\
			<td>Create Folder</td><td><input type = 'text' name='para' id = '2' ></td>\
			<td><input type='submit' name= 'button' value='create folder'></td>\
			</tr>\
		</form>"


print "	<form action='settings_back.py' onSubmit='return finalcheck(3);'><tr>\
		<td>Delete Folder</td><td><input type = 'text' name='para' id = '3'></td>\
		<td><input type='submit' name= 'button'  value='delete folder'></td>\
		</tr></form>"
print "<center>"
print "Please Enter the Input in the form ('Filters_On':'Filters_Folder':'Filters_Value') without quotes"
print "</center>"


print  "<form action='settings_back.py' onSubmit='return finalcheck(4);'><tr>\
		<td>Create Filter</td><td><input type = 'text' name='para' id = '4'></td>\
		<td><input type='submit' name= 'button'  value='Create Filter'>\
		</tr></form>"


print "<form action='settings_back.py' onSubmit='return finalcheck(5);'><tr>\
		<td>Delete Filers</td><td><input type = 'text' name='para' id = '5'></td>\
		<td><input type='submit' name= 'button' value = 'Delete Filter'></td>\
		</tr></form>"

print "</table ></tbody>"
data = ldb.get_filter(email_id)

print "<br><br><br>"

print "<table align = 'center'><tr><td>filter_on</td><td>filter_action</td><td>filter_value</td><tr>"
for d in data:
	arr = ["From","Subject","Priority"]
	print "<tr><td>"+arr[d[1]-1]+"</td><td>"+d[2]+"</td><td>"+d[3]+"</td></tr>"
print "</table>"




print '<script>\
function finalcheck(val){\
    var x1 = document.getElementById(val).value;\
    if (x1 == null || x1 == "") {\
        alert("value must be filled out");\
        x1.focus;\
        return false;\
    }\
    return true;\
}\
</script>\
<noscript>\
<h1>This page needs JavaScript to function properly!!</h1>\
</noscript>'