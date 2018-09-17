# Rough python email body parser code 

import re 
pattern_exp = r'''\<a class="jobtitle tap_item_link" href="([^\;]*)&amp.*>(.*)'''
with open('quoted_text_email.txt') as message_file:
	contents = message_file.read()
	match_object = re.search(pattern_exp,contents)
	print match_object.group(1)
	print match_object.group(2)
	