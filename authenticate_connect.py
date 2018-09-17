# Script to parse emails from indeed.com Alerts


import quopri
import requests
import getpass 
import subprocess
import re
import gmail
import email
import email.message
import imaplib
import json
from pprint import pprint



class emailconnect():
	"""Object - email inbox.
	Methods - Performs Authentication of the email using oauth2
	save the oauth2 script in the same directory as this directory
	"""
	
	
	def __init__(self,userid,clientidfile):
		self.username = userid
		self.clientid = clientidfile
		self.access_token = None
		self.imap = None
		self.folders = None
		self.uids = None
		
	def TokenRunner(self,scriptfile = 'oauth2.py'):
		unm = self.username
		client_id_file = self.clientid 
		with open(client_id_file) as data_file:
			data = json.load(data_file)

		my_clientID=data['installed']['client_id']
		my_client_secret=data['installed']['client_secret']
		refreshtoken = data['installed']['refresh_token']
		scriptrunner = scriptfile + ' --user=' + unm + ' --client_id=' + my_clientID + ' --client_secret=' + my_client_secret + ' --refresh_token=' + refreshtoken
		embedded_rawstr = r"""Access Token: (.*)"""
		cmd=subprocess.Popen(scriptrunner,shell=True,stdout=subprocess.PIPE)
		Access_token=''

		for line in cmd.stdout:
			if 'Access Token:' in line:
				match_token=re.search(embedded_rawstr,line)
				Access_token=match_token.group(1)

		self.access_token = Access_token
		
	def authenticate_login(self):
		GMAIL_IMAP_HOST = 'imap.gmail.com'
		GMAIL_IMAP_PORT = 993
		uname = self.username
		access = self.access_token
		auth_string = 'user=%s\1auth=Bearer %s\1\1' % (uname,access)
		imap_obj = imaplib.IMAP4_SSL(GMAIL_IMAP_HOST, GMAIL_IMAP_PORT)
		imap_auth = imap_obj.authenticate('XOAUTH2', lambda x: auth_string)
		if isinstance(imap_auth,tuple):
			response,authentication_msg = imap_auth
			if 'Success' in authentication_msg[0]:
				print 'Connected...Saved at',imap_obj
				self.imap = imap_obj


# x = emailconnect('sriramchander@gmail.com',r'F:\DataScience\Programming\EmailParser\ClientID.json')
# x.TokenRunner()
# x.authenticate_login()
# print 'Object Details: '
# print x.username
# print x.clientid 
# print x.imap 


