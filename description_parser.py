# Sample Job Description Parser from Emails
import re

def description(filepath):
	file_contents = ''
	company_description_regex = r'''<div class="cmp_description">(((\s)|(.))*?)</div>'''
	jobtitle_regex = r'''<b class="jobtitle"><font size=\"\+1\">(.*)<\/font>'''
	job_description_regex = r'''<span id="job_summary" class="summary">(((\s)|(.))*?)<div class\="result-link-bar-container result-link-bar-viewjob">'''
	output = {}
	
	with open(filepath,'r') as jobpage_source:
		file_contents = jobpage_source.read()
		file_contents = file_contents.strip()
		# file_contents = file_contents.replace('\n','')
		print type(file_contents)
		print file_contents[:50]
		print re.findall('\r\n',file_contents)
		# print re.findall('\n',file_contents)
		# print file_contents
		comp_description = re.findall(company_description_regex,file_contents)[0][0]
		print type(comp_description)
		output['Company Description'] = comp_description[0]
		print type(output['Company Description'])
		output['JobTitle'] = str(re.findall(jobtitle_regex,file_contents)[0])
		output['JobDescription'] = str(re.findall(job_description_regex,file_contents)[0])
		output['JobDescription'] = output['JobDescription'].replace('<br>','\n')
	return output
		
jobdescription = description('samplefile.txt')
print jobdescription