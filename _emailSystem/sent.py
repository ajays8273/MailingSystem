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



localtime = time.asctime( time.localtime(time.time()) )
print "	Local current time :", localtime
print '</br>'

with open('menu.html') as f:
  print f.read()

#print environ

current_folder = "sent"	

folders = ldb.get_all_folder(email_id)
print '<ul>'
for row in folders :
		print '<ul><li><a href="inbox.py?folder='+row[0]+'" onclick= '+"'delete_cookies()'"+' >'+row[0]+'</a></li>'
print '</ul>'
print '</br>'

unique = os.environ.get('QUERY_STRING')
#print unique
if(unique):
	unique_id = str(unique)[7:]
	current_folder = unique_id

#print "move to "
#print '<select>'
#for row in folders :
		#print '<option value=' + row[0] + '>'+ row[0]+'</option>'
#print '</select></br>'

#print int(cookie['page'].value)+10
n = int(cookie['page'].value)+10
p = int(cookie['page'].value)-10

number_of_mails = int(ldb.get_email_count (email_id,current_folder,"s")[0])
#print number_of_mails , n , p

print '</br>'
inbox_mails = ldb.get_emails(email_id,current_folder,n-10 ,n,"s")
print '<table align = "left"><tr>\
		<td colspan=2 align="left"><h3>Sent_Mails</h3></td></tr>\
		<tbody>'
#print '</br><tr>'
if(n <= number_of_mails ):
	print '<td><a href="redirect_sent_page.py?page='+str(n)+'&'+'folder='+current_folder+'">next</a></td>'
if(p>=0):
	print '<td><a href="redirect_sent_page.py?page='+str(p)+'&'+'folder='+current_folder+'">previous</a></td>'
print '</tr>'
print '<tr><td ><font size="4" color="red">to</td>\
			<td><font size="4" color="red">sub</td>\
			<td><font size="4" color="red">priority</td>\
			<td ><font size="4" color="red">time</td></tr>'
for row in inbox_mails :
			unique_id = row[0]+'@'+row[1]+'@'+str(row[5])
			print '<tr><td ><font size="4" color="blue">'+ row[1]+'</td>\
			<td><font size="4" color="blue"> <a href="show.py?data='+ unique_id+ '">'+ row[2]+'</a> </td>\
			<td><font size="4" color="blue">'+ row[4]+'</td>\
			<td><font size="4" color="blue">'+ str(row[5])+'</td>\
			<td><font size="4" color="blue"> <a href="delete.py?data='+ unique_id+"@delete"+ '" >delete</a> </td>'
			print '<form method = "post" action="move.py">'
			print '<td><select name ="folder_move">'
			for ro in folders :
					print '<option value=' +'"'+ unique_id + "@" + str(ro[0]) +'"'+'>'+ ro[0]+'</option>'
			print '</select></td>\
			<td><input type="submit" name="request"  value="move"></td>\
			</form>'
			#print '<td>' + unique_id + '</td></tr>'
print '</tbody>'