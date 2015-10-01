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
print "</br>"

with open('menu.html') as f:
  print f.read()

folders = ldb.get_all_folder(email_id)
print '<ul>'
for row in folders :
		print '<ul><li><a href="inbox.py?folder='+row[0]+'" onclick= '+"'delete_cookies()'"+' >'+row[0]+'</a></li>'
print '</ul>'
print '</br>'


print '  <script type="text/javascript" src="/_emailSystem/cal.js"></script>\
    <!--Load Script and Stylesheet -->\
    <script type="text/javascript" src="/_emailSystem/jquery.simple-dtpicker.js"></script>\
    <link type="text/css" href="/_emailSystem/jquery.simple-dtpicker.css" rel="stylesheet" />\
		<br><br><br><table><tbody valign="top" >\
		<form action="compose.py" method= "post" enctype="multipart/form-data">\
		<tr>\
		<td>To:</td>\
		<td><input type="text"  name="rec_email" id = "1"></td>\
		<tr>\
		<tr>\
		<td>Subject:</td>\
		<td><input type="text" name="subject"></td>\
		</tr>\
		<tr>\
		<td>Priority:</td>\
		<td><select name ="Prior">\
			  <option value="high">High</option>\
			  <option value="medium">Medium</option>\
			  <option value="low">Low</option>\
			  </select></td></tr>\
			  <tr>\
		<tr>\
		<td>Message:</td>\
		<td ><textarea name="message" rows="10" cols="50" ></textarea></td>\
		</tr>\
		<tr>\
		<td>Select a file: </td><td><input type="file" name="file"></td>\
		</tr>\
		<tr>\
		<td></td><td><input type="submit" value="Send" name="Send" onclick = "return check()" >\
		<input type="submit" value="Save_Draft" name="Save_Draft" onclick = "return check()"></td>\
		</tr>\
		<tr>\
		<td>\
		</td><td>\
		<input type="text" name="date2" class = "datetime" value="2012/01/01 10:00">\
		</td>\
		<td><input type="submit" value="schedule_draft" name ="schedule_draft" onclick = "return check()"></td>\
		</tr>\
</form>\
</tbody>\
</table>\
<script type="text/javascript">\
		$(function(){\
			$("*[name=date2]").appendDtpicker({"inline": true});\
		});\
	</script>'




print '<script>\
function check(){\
    var x1 = document.getElementById("1").value;\
    if (x1 == null || x1 == "") {\
        alert("value must be filled out");\
        x1.focus;\
        return false;\
    }\
    var re = new RegExp("^[a-zA-Z0-9_]*$");\
    if(!re.test(x1)){alert("Not a valid email-address!!")};\
    return re.test(x1);\
}\
</script>\
<noscript>\
<h1>This page needs JavaScript to function properly!!</h1>\
</noscript>'