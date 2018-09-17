# EmailParser Main file
from authenticate_connect import emailconnect
from emailparser import EmailParser

def main():
	
	username = raw_input('Please Enter Your Username: ')
	clientidfile = raw_input('Enter the ClientID json file: ')
	parsers = raw_input('Enter the Regex File path to pull data from your emails: ')
	RFC_searchstring = raw_input('Enter the RFC Search Strings to set the type of emails: ')
	Inboxname = raw_input('Folder name: ')
	userobject = EmailParser(username,clientidfile)
	