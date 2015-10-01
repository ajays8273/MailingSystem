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
draft_id = unique.split('=')[1]
ldb.delete_draft(draft_id)
print 'Content-type:text/html\r\n'+'Location: %s' % "draft.py"	
print "\r\n\r\n"