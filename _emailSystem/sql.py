#!/usr/bin/python

import MySQLdb
import hashlib
class sqldb:
	
	def __init__(self):
                servername = "localhost"
                username = "root"
                password = "root"
                database = "email_system"
		self.db = MySQLdb.connect(servername,username,password,database);
		self.cursor = self.db.cursor();
		self.cursor.execute("CREATE TABLE IF NOT EXISTS `folder_table` ( `email_id` VARCHAR(200) NOT NULL,`folder` VARCHAR(45) NOT NULL,PRIMARY KEY (`email_id`, `folder`));");
		self.cursor.execute("CREATE TABLE IF NOT EXISTS `login_table` (  `email_id` VARCHAR(200) NOT NULL,`password` VARCHAR(100) NOT NULL,`user_name` VARCHAR(45) NOT NULL ,`university` VARCHAR(45) NOT NULL,`dob` DATE NOT NULL,PRIMARY KEY (`email_id`));");
		self.cursor.execute("CREATE TABLE IF NOT EXISTS `email_table` (`sender_email` VARCHAR(200) NOT NULL,`reciever_email` VARCHAR(200) NOT NULL,`subject` VARCHAR(45) NULL,`attachement` BLOB NULL,`priority` ENUM('low','medium','high') NOT NULL,`time_stamp` TIMESTAMP NOT NULL,`flag` BIT(1) NOT NULL,`sender_folder` VARCHAR(45) NULL,`reciever_folder` VARCHAR(45) NULL,`mail_body` TEXT NULL,PRIMARY KEY (`sender_email`, `reciever_email`, `time_stamp`));");
		self.cursor.execute("CREATE TABLE IF NOT EXISTS `schedule_draft_table` (  `sender_email` VARCHAR(200) NOT NULL, `receiver_email` VARCHAR(200) NOT NULL,  `subject` VARCHAR(45) NULL,  `priority` ENUM('low','medium','high') NOT NULL,  `mail_body` TEXT NULL,  `attachement` BLOB NULL,  `schedule_time` DATETIME NOT NULL,  PRIMARY KEY (`sender_email`, `receiver_email`, `schedule_time`));");
		self.cursor.execute("CREATE TABLE IF NOT EXISTS `draft_table` (  `sender_email` VARCHAR(200) NOT NULL,  `reciever_email` VARCHAR(200) NOT NULL,  `subject` VARCHAR(45) NULL,  `priority` ENUM('low','medium','high') NOT NULL,  `mail_body` TEXT NULL,  `attachement` BLOB NULL,  `draft_id` INT NOT NULL AUTO_INCREMENT,  PRIMARY KEY (`draft_id`));");
		self.cursor.execute("CREATE TABLE IF NOT EXISTS `filter_table` (  `email_id` VARCHAR(200) NOT NULL,  `filter_type` INT NOT NULL,  `action` VARCHAR(100) NOT NULL,  `filter_value` VARCHAR(100) NOT NULL,  PRIMARY KEY (`email_id`, `filter_type`, `filter_value`));");
		
	def check_user(self,emailid,passwd):
		self.cursor.execute("SELECT * FROM login_table WHERE email_id = '"+emailid+"' and password = '"+passwd+"';");
		data = self.cursor.fetchone()
		if(data):
			return True
		else:
			return False

        def find_user(self,emailid):
                query = "SELECT COUNT(*) FROM login_table where email_id = '%s'" % (emailid)
                try:
			self.cursor.execute(query);
			self.db.commit()
			data = self.cursor.fetchone()
			return data[0]==0
		except:
			#print "error occured"
			self.db.rollback()
			return True
		    
	def check_hash(self,hashvalue,emailid):
		self.cursor.execute("SELECT * FROM login_table WHERE email_id = '"+emailid+"' ;");
		data = self.cursor.fetchone()
		# print data[0],data[1]
		if(data):
			hashObj = hashlib.md5()
			hashObj.update(data[0]+data[1])
			hashstring = hashObj.hexdigest()
			if(hashstring == hashvalue):
				return True
			else:
				return False
		else:
			return False
		    
	def add_user(self,email_id,password,user,university,dob):
		query = """insert into login_table (email_id,password,user_name,university,dob) values ('%s','%s','%s' ,'%s','%s') """ % (email_id,password,user,university,dob) ;
		#print query
		try:
			self.cursor.execute(query);
			self.db.commit()
		except:
			#print "error occured"
			self.db.rollback()
	
	
	def delete_user(self,email_id):
                query = "DELETE from login_table where email_id = '%s' ; " % (email_id)
		try :
                    self.cursor.execute(query);
                    self.db.commit()
                except:
                    #print "error occured"
                    self.db.rollback()
                
        def send_email(self,email_obj):
                query = """insert into email_table (sender_email,reciever_email,subject,attachement,priority,time_stamp,flag,sender_folder,reciever_folder,mail_body) values ('%s','%s','%s','%s','%s','%s',%s,'%s','%s','%s') """ % (email_obj['sender_email'],email_obj['reciever_email'],email_obj['subject'],email_obj['attachement'],email_obj['priority'],email_obj['time_stamp'],email_obj['flag'],email_obj['sender_folder'],email_obj['receiver_folder'],email_obj['mail_body'])
                
                try :
                        self.cursor.execute(query)
                        self.db.commit()
                except:
                       # print "error occured"
                        self.db.rollback()

        
        def create_folder(self,email_id,folder):
                query = """insert into folder_table (email_id,folder) values ('%s','%s') """ % (email_id,folder)
                try :
                        self.cursor.execute(query)
                        self.db.commit()
                except:
                        #print "error occured"
                        self.db.rollback()

        def create_filter(self,filter_obj):
                query = """insert into filter_table (email_id,filter_type,action,filter_value) values ('%s',%s,'%s','%s') """ % (filter_obj['email_id'],filter_obj['filter_type'],filter_obj['action'],filter_obj['filter_value'])
                try :
                        self.cursor.execute(query)
                        self.db.commit()
                except:
                        #print "error occured"
                        self.db.rollback()

        def schedule_draft(self,sd_obj):
                query = """ insert into schedule_draft_table (sender_email,receiver_email,subject,priority,mail_body,attachement,schedule_time) values ('%s','%s','%s','%s','%s','%s','%s') """ % (sd_obj['sender_email'],sd_obj['receiver_email'],sd_obj['subject'],sd_obj['priority'],sd_obj['mail_body'],sd_obj['attachement'],sd_obj['schedule_time'])
                #print query
                try :
                        self.cursor.execute(query)
                        self.db.commit()
                except:
                        #print "error occured"
                        self.db.rollback()
        
        def save_draft(self,sd_obj):
                query = """ insert into draft_table (sender_email,reciever_email,subject,priority,mail_body,attachement) values ('%s','%s','%s','%s','%s','%s') """ % (sd_obj['sender_email'],sd_obj['receiver_email'],sd_obj['subject'],sd_obj['priority'],sd_obj['mail_body'],sd_obj['attachement'])
		try :
                        self.cursor.execute(query)
                        self.db.commit()
                except:
                        #print "error occured"
                        self.db.rollback()
        
        def get_all_folder(self,email_id):
                query = """select folder from `folder_table` where email_id = '%s' """ % (email_id)
                try :
                        self.cursor.execute(query)
                        self.db.commit()
                        data = self.cursor.fetchall()
                        return data
                except:
                        #print "error occured"
                        self.db.rollback()
                        return False
        def get_filter (self,email_id):
                query = """select * from `filter_table` where email_id = '%s' """ % (email_id)
                try :
                        self.cursor.execute(query)
                        self.db.commit()
                        data = self.cursor.fetchall()
                        return data
                except:
                        #print "error occured"
                        self.db.rollback()
                        return False

        def get_emails (self, email_id,folder,From,To,who):
                if(who=="s"):
                        query = """ select * from `email_table` where sender_email = '%s' and  sender_folder = '%s' ORDER BY time_stamp DESC LIMIT %s,%s """ % (email_id,folder,From-1,To-From+1)
                else:
                        query = """ select * from `email_table` where reciever_email = '%s' and  reciever_folder = '%s' ORDER BY time_stamp DESC LIMIT %s,%s """ % (email_id,folder,From-1,To-From+1)
                #print query
                try :
                        self.cursor.execute(query)
                        self.db.commit()
                        data = self.cursor.fetchall()
                        return data
                except:
                        #print "error occured"
                        self.db.rollback()
                        return False

        def get_email_count (self, email_id,folder,who):
                if(who=="s"):
                        query = """ select count(*) from `email_table` where sender_email = '%s' and sender_folder = '%s' """ % (email_id,folder)
                else: 
                        query = """ select count(*) from `email_table` where reciever_email = '%s' and reciever_folder = '%s' """ % (email_id,folder)
                try:
                        self.cursor.execute(query)
                        self.db.commit()
                        data = self.cursor.fetchone()
                        return data
                except:
                        #print "error occured"
                        self.db.rollback()
                        return False
        
        def change_folder_email(self, sender, reciever, TimeStamp, who , folder):
                if(who=="s"):
                        query = """update email_table set sender_folder = '%s', time_stamp = time_stamp where sender_email = '%s' and reciever_email = '%s' and time_stamp = '%s' """ % (folder,sender, reciever, TimeStamp)
                else:
                        query = """update email_table set reciever_folder = '%s', time_stamp= time_stamp where sender_email = '%s' and reciever_email = '%s' and time_stamp = '%s' """ % (folder,sender, reciever, TimeStamp)
                #print query
                try :
                        self.cursor.execute(query)
                        self.db.commit()
                except:
                        #print "error occured"
                        self.db.rollback()

                query = """ delete from `email_table` where sender_folder = 'delete' and reciever_folder = 'delete' """
                try :
                        self.cursor.execute(query)
                        self.db.commit()
                except:
                        #print "error occured"
                        self.db.rollback()
        def pick_schedule_draft(self, TimeStamp):
                query = """ select * from `schedule_draft_table` where schedule_time <= '%s' """ % (TimeStamp)
                try:
                        self.cursor.execute(query)
                        self.db.commit()
                        data = self.cursor.fetchall()
                        return data
                except:
                        #print "error occured"
                        self.db.rollback()
                        
        def delete_schedule_draft(self, TimeStamp):
                query = """ delete from `schedule_draft_table` where schedule_time <= '%s' """ % (TimeStamp)
                #print query
                try:
                        self.cursor.execute(query)
                        self.db.commit()
                except:
                        #print "error occured"
                        self.db.rollback()

        def get_filter_action(self, sender_email, reciever_email, subject, priority):
                data = self.get_filter(reciever_email)
                action = ""
                for filters in data:
                        if(filters[1] == 1 and sender_email == filters[3] and (action == "" or action == filters[2])):
                                action = filters[2]
                        elif(filters[1] == 2 and subject == filters[3] and (action == "" or action == filters[2])):
                                action = filters[2]
                        elif(filters[1] == 3 and priority == filters[3] and (action == "" or action == filters[2])):
                                action = filters[2]
                        elif( ((filters[1] == 1 and sender_email == filters[3]) or (filters[1] == 2 and subject == filters[3]) or (filters[1] == 3 and priority == filters[3])) and action!="" ):
                                action = "inbox"
                if(action == ""):
                        action = "inbox"
                return action
        def get_mail_body(self, mail_to, mail_from , timestamp):
                query = """ select * from `email_table` where sender_email = '%s' and reciever_email = '%s' and time_stamp = '%s' """ % (mail_from,mail_to,timestamp)
                #print query
                try:
                        self.cursor.execute(query)
                        self.db.commit()
                        data = self.cursor.fetchone()
                        return data
                except:
                        #print "error occured"
                        self.db.rollback()
        def get_draft_from_id(self,draft_id):
                query = """ select * from `draft_table` where draft_id = '%s' """ % (draft_id)
                #print query
                try:
                        self.cursor.execute(query)
                        self.db.commit()
                        data = self.cursor.fetchone()
                        return data
                except:
                        #print "error occured"
                        self.db.rollback()
        def get_drafts(self, email_id,From,To):
                query = """ select * from `draft_table` where sender_email = '%s' ORDER BY draft_id ASC LIMIT %s,%s """ %(email_id,From-1,To-From+1)
                #print query
                try:
                        self.cursor.execute(query)
                        self.db.commit()
                        data = self.cursor.fetchall()
                        return data
                except:
                        #print "error occured"
                        self.db.rollback()
        def delete_draft(self, draft_id):
                query = """ delete from `draft_table` where draft_id = '%s' """ % (draft_id)
                try:
                        self.cursor.execute(query)
                        self.db.commit()
                        data = self.cursor.fetchall()
                        return data
                except:
                        #print "error occured"
                        self.db.rollback()
        def get_draft_count(self, email_id):
                query = """ select count(*) from `draft_table` where sender_email = '%s' """ % (email_id)
                try:
                        self.cursor.execute(query)
                        self.db.commit()
                        data = self.cursor.fetchone()
                        return data
                except:
                        #print "error occured"
                        self.db.rollback()
        
        def get_schedule_draft_count(self, email_id):
                query = """ select count(*) from `draft_table` where sender_email = '%s' """ %(email_id)
                try:
                        self.cursor.execute(query)
                        self.db.commit()
                        data = self.cursor.fetchone()
                        return data
                except:
                        #print "error occured"
                        self.db.rollback()
        def get_schedule_drafts(self, email_id,From,To):
                query = """ select * from `schedule_draft_table` where sender_email = '%s' ORDER BY schedule_time ASC LIMIT %s,%s """ % (email_id, From-1, To-From+1)
                try:
                        self.cursor.execute(query)
                        self.db.commit()
                        data = self.cursor.fetchall()
                        return data
                except:
                        #print "error occured"
                        self.db.rollback()
                        
        def get_smail(self, sender_email, reciever_email, time):
                query = """ select * from `schedule_draft_table` where sender_email = '%s' and receiver_email = '%s' and schedule_time = '%s' """ % (sender_email, reciever_email, time)
                try:
                        self.cursor.execute(query)
                        self.db.commit()
                        data = self.cursor.fetchone()
                        return data
                except:
                        #print "error occured"
                        self.db.rollback()
        def delete_smail(self, sender_email,reciever_email,time):
                query = """ delete from `schedule_draft_table` where sender_email = '%s' and receiver_email = '%s' and schedule_time = '%s' """ % (sender_email, reciever_email, time)
              #  print query
                try:
                        self.cursor.execute(query)
                        self.db.commit()
                        data = self.cursor.fetchone()
                        return data
                except:
                        #print "error occured"
                        self.db.rollback()
        def change_password(self, email_id, newpss):
                query = """ update `login_table` set password = '%s' , dob = dob where email_id = '%s' """ % (newpss, email_id)
                try:
                        self.cursor.execute(query)
                        self.db.commit()
                        data = self.cursor.fetchone()
                        return data
                except:
                        #print "error occured"
                        self.db.rollback()
        def delete_folder(self, email_id , folder):
                query = """ delete from `folder_table` where email_id = '%s' and folder = '%s' """ % (email_id,folder)
                #print query
                try:
                        self.cursor.execute(query)
                        self.db.commit()
                        data = self.cursor.fetchone()
                        return data
                except:
                        #print "error occured"
                        self.db.rollback()
        def delete_filter(self, filter_obj):
                query = """ delete from `filter_table` where email_id = '%s' and filter_type = %s and filter_value = '%s' """ % (filter_obj['email_id'],filter_obj['filter_type'],filter_obj['filter_value'])
                #print query
                try:
                        self.cursor.execute(query)
                        self.db.commit()
                        data = self.cursor.fetchone()
                        return data
                except:
                        #print "error occured"
                        self.db.rollback()
