# Script for Parsing Email Body 
import re 
def parse_email_body(filename,headers):
	
	
	with open(filename,'r') as emailfile:
		filecontents = emailfile.read()
		
	job_details = []
	matches = []
	viewjob_link = r'''http://indeed.com/viewjob?jk='''
	# jk = ebb5eb3f0606206a
	
	for field in headers: 
		matches = re.findall(headers[field],filecontents)
		for match in matches:
			jobrecord = {}
			jobrecord['Date'] = 'Wed, 16 Sep 2015 07:33:59 -0700 (PDT)'
			jobrecord['Subject'] = '30+ new data analyst opportunities in California'
			jobrecord[field] = match
			job_details.append(jobrecord)
	return job_details

headers = {}
headers['JobKey'] =  r'''\<a class="jobtitle tap_item_link" href=".*jk=([^\;]*)&amp.*'''
job = parse_email_body('quoted_text_email.txt',headers)

for j in job:
	print j 