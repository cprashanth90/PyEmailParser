# sample program to parse indeed email saved as text file
# The parsed fields are seen after the message content is decoded. 

import quopri
import re 
import requests
import codecs
import sys
reload(sys)

# def indeed_email_parse(filepath):
	# mail_content = ''
	# jobtitle_regexp = r'''<a class="jobtitle tap_item_link" href=".*">(.*)</a>'''
	# jobkey_regexp = r'''http\:\/\/www\.indeed\.com\/.*jk\=([^;]*)\&amp'''
	# job_companies = r'''\<span class=\"job_company\">(.*)<\/span>'''
	# job_posting_time = r'''<span class="job_age" style="color:#666;"><a href class="nolink".*>(.*)</a>'''
	# job_location = r'''<span style="color:#666;"><a href class="nolink".*">(.*)</a></span></div>'''
	
	# jobtitle = []
	# jobkeys = []
	# companyname = []
	# posting_time = []
	# location = []
	
	# with open(filepath,'r') as emailfile:
		# mail_content = quopri.decodestring(emailfile.read())
		# jobtitle = re.findall(jobtitle_regexp,mail_content)
		# jobkeys = re.findall(jobkey_regexp,mail_content)
		# companyname = re.findall(job_companies,mail_content)
		# posting_time = re.findall(job_posting_time,mail_content)
		# location = re.findall(job_location,mail_content)
		
	# print location
	# print companyname
	# print jobkeys 
	# print jobtitle
url = r'''http://www.indeed.com/viewjob?jk=10fb3a4a0ab863d2'''
sys.setdefaultencoding('utf-8')
r = requests.get(url)
text_html = r.text
assert isinstance(text_html,unicode)
description_pattern = r'''<span id="job_summary" class="summary">([^\t]*)<div class="result-link-bar-container result-link-bar-viewjob">'''
# print str(text_html)
unicode_content = text_html.decode('utf-8')

job_page_content = str(unicode_content)
content_list = job_page_content.split('\t')
job_page_content = ''

for contents in content_list:
	job_page_content = job_page_content + contents

job_description = re.findall(description_pattern,job_page_content)
print type(job_description)
print len(job_description)
print job_description[0].rstrip()

# xml_content = unicode_content.encode('ascii', 'xmlcharrefreplace')