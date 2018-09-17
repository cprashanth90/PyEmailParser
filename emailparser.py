from authenticate_connect import emailconnect
import email
import re 
import quopri
import csv
import requests
import sys


class Emailparser():
	
	def __init__(self,username,clientidfile):
		self.connection = self.get_connection(username,clientidfile)
		self.folders = None
		self.regex_list = {}
		self.uids = None 
	
	def set_regexes(self):
		regex_patterns = {}
		regex_patterns['JobApplicationPage'] = r'''\<a class="jobtitle tap_item_link" href="([^\;]*)&amp.*'''
		regex_patterns['Jobkey'] = r'''\<a class="jobtitle tap_item_link" href=".*jk=([^\;]*)&amp.*'''
		regex_patterns['Jobtitle'] = r'''\<a class="jobtitle tap_item_link" href=.*>(.*)<\/a>'''
		regex_patterns['JobPostedOn'] = r'''\<span class="job_age" style="color\:\#666\;">[\r\n]*<a href.*>(.*)<\/a>'''
		regex_patterns['Companyname'] = r'''\<span class="job_company">(.*)</span>'''
		regex_patterns['Job_location'] = r'''\<span style="color\:\#666\;">[\r\n]*<a href.*>(.*)<\/a>'''
		self.regex_list = regex_patterns
	
	def get_connection(self,user,clientid):
		connection_obj = emailconnect(user,clientid)
		connection_obj.TokenRunner()
		connection_obj.authenticate_login()
		return connection_obj.imap 
		
	
	def email_folders(self):
		folders = []
		imap_obj = self.connection
		status,raw_folder_list = imap_obj.list()
		parse_folder_name = r'''\"\/\" \"(.*)\"'''
		for entry in raw_folder_list:
			if '''"/"''' in entry:
				match_val = re.search(parse_folder_name,entry)
				folders.append(match_val.group(1))
		self.folders = folders
		return folders

	def search_email(self,folder_name,search_string):
		imapobj = self.connection
		imapobj.select(folder_name,readonly = True)
		count = 0
		response,msg_data_id = imapobj.search(None,search_string)
		self.uids = msg_data_id[0].split()
		return msg_data_id[0].split()

	def parse_body_email(self):
		# Make content_items a List of Dicts and then convert it into a tuple object only while writing records into file/database.
		
		content_items = {}
		email_recorddata = []
		message_list = self.uids
		message_list = message_list[len(message_list) - 15:]
		imap_obj = self.connection
		regexlist = self.regex_list
		additional_keys = ['DateReceived','IndeedJobPage','Alert_Name']
		
		indeed_viewjob_link = r'''http://indeed.com/viewjob?jk='''
		
		for message_num in reversed(message_list):
			item_matches = []
			jobkey_list = []
			print 'Fetching Email Data...'
			response,message_data = imap_obj.fetch(message_num,'(RFC822)')
			msg_string = email.message_from_string(message_data[0][1])
			print 'On Date Received: ', msg_string['Date']
			itemvalues = ''
			if msg_string.is_multipart():
				for payload in msg_string.get_payload():
					itemvalues = payload.get_payload()
			else:
				itemvalues = msg_string.get_payload()
			
			itemvalues = quopri.decodestring(itemvalues)
			item_header = ''
			
			 
			for field in self.regex_list:
				
				if field not in content_items:
					content_items[field] = []
					
				item_matches = re.findall(self.regex_list[field],itemvalues)
				
				if field == 'Jobkey':
					jobkey_list = item_matches
				
				for data in item_matches:
					content_items[field].append(data)
			
			for add_key in additional_keys:
				if add_key not in content_items:
					content_items[add_key] = []
			
			for jobkey in jobkey_list:
				content_items['IndeedJobPage'].append(indeed_viewjob_link + jobkey)
				content_items['DateReceived'].append(msg_string['Date'])
				content_items['Alert_Name'].append(msg_string['Subject'])
				
		first_key = content_items.keys()[0]
		keys_length = len(content_items[first_key])
		print 'Cleaning up all data..Converting into Records...'
		for index in range(0,keys_length):
			record = []
			for key in iter(content_items):
				try:
					record.append(content_items[key][index])
				except IndexError:
					record.append('')
					
				
			record = tuple(record)	
			email_recorddata.append(record)
		return email_recorddata,content_items.keys()
		
	def parse_email(self):
		content_items = {}
		email_recorddata = []
		message_list = self.uids
		message_list = message_list[len(message_list) - 25:]
		imap_obj = self.connection
		regexlist = self.regex_list
		additional_keys = ['DateReceived','IndeedJobPage','Alert_Name']
		
		indeed_viewjob_link = r'''http://indeed.com/viewjob?jk='''
		regex_jobkey = r'''\<a class="jobtitle tap_item_link" href=".*jk=([^\;]*)&amp.*'''
		for message_num in reversed(message_list):
			item_matches = []
			jobkey_list = []
			print 'Fetching Email Data...'
			response,message_data = imap_obj.fetch(message_num,'(RFC822)')
			msg_string = email.message_from_string(message_data[0][1])
			if msg_string.is_multipart():
				for payload in msg_string.get_payload():
					itemvalues = payload.get_payload()
			else:
				itemvalues = msg_string.get_payload()
			
			itemvalues = quopri.decodestring(itemvalues)
			item_header = ''
			matches = re.findall(regex_jobkey,itemvalues)
			for match in matches:
				jobrecord = {}
				jobrecord['Date'] = msg_string['Date']
				jobrecord['Subject'] = msg_string['Subject']
				jobrecord['Jobkey'] = match
				email_recorddata.append(jobrecord)
		return email_recorddata
		
		
	def job_description(self,IndeedJobKeyList):
		reload(sys)
		sys.setdefaultencoding('utf-8')
		getURL = r'''http://indeed.com/viewjob?jk='''
		regexpattern = r'''<b class\=\"jobtitle\"><font size\=\"\+1\">(.*)</font></b>'''
		location_regex = r'''<span class="company">(.*)</span>'''
		jobtitle = ''
		output = []
		for job in IndeedJobKeyList:
			
			jobdescription = ''
			url = getURL + job['Jobkey']
			job_request = requests.get(url)
			jobdescription = job_request.text
			jobdescription = jobdescription.decode('utf-8')
			
			jobtitle = re.findall(regexpattern,str(jobdescription))
			location = re.findall(regexpattern,str(jobdescription))
			
			if len(jobtitle) > 0:
				job['JobTitle'] = jobtitle[0]
			else:
				job['JobTitle'] = ''
			if len(location) > 0:
				job['Location'] = location[0]
			else:
				job['Location'] = ''
				
			output.append(job) 
		return output
		


RFC_searchstring = raw_input('Enter the RFC Search Strings to set the type of emails: ')
Inboxname = raw_input('Folder name: ')
x = Emailparser('sriramchander@gmail.com',r'F:\DataScience\Programming\EmailParser\ClientID.json')
y = x.email_folders()
x.set_regexes()

list_ids = x.search_email(Inboxname,RFC_searchstring)
# email_data,headers = x.parse_body_email()
f = x.parse_email()
# print len(email_data)
g = x.job_description(f)
print type(f)
print len(f)
# for item in g:
	# print 'Message Item: Received on', item['Date']
	# print 'Job Title: ', item['JobTitle']
	# print 'Posting Location: ', item['Location']
	
for item in g:
	if item['JobTitle'] == '':
		print item

# From Stackoverflow - http://stackoverflow.com/questions/3820312/python-write-a-list-of-tuples-to-a-file

# with open('outfile.csv', "w") as out_file:
	# dialect = csv.register_dialect('custom', lineterminator = '\n',skipinitialspace = True)
	# writer = csv.writer(out_file,dialect = 'custom')
	# writer.writerow(tuple(headers))
	# for tup in email_data:
		# writer.writerow(tup)
	# out_file.close()


