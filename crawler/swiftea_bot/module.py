#!/usr/bin/python3

"""Define several functions for all crawler's class."""

from time import strftime
from os import path, mkdir, remove, listdir
import sys

import swiftea_bot.data as data

def tell(message, error_code='', severity=1):
	"""Manage newspaper.

	Print in console that program doing and save a copy with time in event file.

	:param message: message to print and write
	:type message: str
	:param error_code: (optional) error code, if given call errors() with given message
	:type error_code: int
	:param severity: 1 is default severity, -1 add 4 spaces befor message,
		0 add 2 spaces befor the message, 2 uppercase and underline message.
	:type severity: int

	"""
	msg_to_print = message[:132]
	message = message.capitalize()
	if error_code != '':
		errors(message, error_code)

	if severity == -1:
		print('    ' + message[:127].lower())
	elif severity == 0:
		print('  ' + message[:129].lower())
	elif severity == 1:
		print(msg_to_print.capitalize())
	elif severity == 2:
		print(msg_to_print.upper())
		print(''.center(len(msg_to_print), '='))

	with open(data.FILE_NEWS, 'a') as myfile:
		myfile.write(strftime('%d/%m/%y %H:%M:%S') + str(error_code) + ' ' + message + '\n')

def errors(message, error_code):
	"""Write the error report with the time in errors file.

	Normaly call by tell() when a error_code parameter is given.

	:param message: message to print and write
	:type message: str
	:param error_code: error code
	:type error_code: int

	"""
	with open(data.FILE_ERROR, 'a') as myfile:
		myfile.write(str(error_code) + ' ' + strftime("%d/%m/%y %H:%M:%S") + ': ' + message + '\n')

def quit_program():
	"""Function who manage end of prgoram."""
	tell('end\n', 0)
	sys.exit()

def create_dirs():
	"""Manage crawler's runing.

	Test lot of things:
		create config directory\n
		create doc file if  doesn't exists\n
		create config file if it doesn't exists\n
		create links directory if it doesn't exists\n
		create index directory if it doesn't exists\n

	"""
	# Create directories if they don't exist:
	if not path.isdir(data.DIR_CONFIG):
		mkdir(data.DIR_CONFIG)
	if not path.isdir(data.DIR_DATA):
		mkdir(data.DIR_DATA)
	if not path.isdir(data.DIR_OUTPUT):
		mkdir(data.DIR_OUTPUT)
	if not path.isdir(data.DIR_INDEX):
		mkdir(data.DIR_INDEX)

def create_doc():
	"""Create doc file if it doesn't exist and if it was modified."""
	if not path.exists(data.FILE_DOC):
		with open(data.FILE_DOC, 'w') as myfile:
			myfile.write(data.ERROR_CODE_DOC)
	else:
		with open(data.FILE_DOC, 'r') as myfile:
			content = myfile.read()
		if content != data.ERROR_CODE_DOC:
			remove(data.FILE_DOC)
		with open(data.FILE_DOC, 'w') as myfile:
			myfile.write(data.ERROR_CODE_DOC)

def def_links():
	"""Create directory of links if it doesn't exist

	Ask to user what doing if there isn't basic links.
	Create a basic links file if user what it.

	"""
	if not path.isdir(data.DIR_LINKS):
		mkdir(data.DIR_LINKS)
		print("""No links directory,
1: let programm choose a list...
2: fill a file yourself...
(see doc.txt file in config)""")
		rep = input("What's your choice ? (1/2) : ")
		if rep == '1':
			# Basic links
			with open(data.FILE_BASELINKS, 'w') as myfile:
				myfile.write(data.BASE_LINKS)
		elif rep == '2':
			open(data.FILE_BASELINKS, 'w').close()
			print("""
Create a file '0' without extention who contains a list of 20 links maximum.
They must start with 'http://' or 'https://' and no ends with '/'.
Choose popular websites.
Press enter when done.""")
			input()
		else:
			print('Please enter 1 or 2.')
			quit()

def is_index():
	"""Check if there is a saved inverted-index file.

	:return: True if there is one

	"""
	if path.exists(data.FILE_INDEX):
		return True
	else:
		return False

def dir_size(source):
	#total_size = path.getsize(source)
	total_size = int()
	for item in listdir(source):
		itempath = path.join(source, item)
		if path.isfile(itempath):
			total_size += path.getsize(itempath)
		elif path.isdir(itempath):
			total_size += dir_size(itempath)
	return total_size

def can_add_doc(docs, new_doc):
	"""to avoid documents duplicate, look for all url doc.

	:param docs: the documents to check
	:type docs: list
	:param new_doc: the doc to add
	:type new_doc: dict
	:return: True if can add the doc

	"""
	for doc in docs:
		if doc['url'] == new_doc['url']:
			return False
	return True

def remove_duplicates(old_list):
	"""Remove duplicates from a list.

	:param old_list: list to clean
	:type old_list: list
	:return: list without duplicates

	"""
	new_list = list()
	for elt in old_list:
		if elt not in new_list:
			new_list.append(elt)
	return new_list

def stats_webpages(begining, end):
	"""Write the time in second to crawl 10 webpages.

	:param begining: time before starting crawl 10 webpages
	:type begining: int
	:param end: time after crawled 10 webpages
	:type end: int

	"""
	delta = end - begining  # Time to crawl ten webpages
	time = delta / 10  # Time in second to crawl 10 webpages
	nb_webpages = 60 / time  # number of webpages crawled in 1 minute
	with open(data.DIR_DATA + 'stat_webpages', 'a') as myfile:
		myfile.write(str(nb_webpages) + '\n')

def convert_keys(inverted_index):
	"""Convert str words keys into int from inverted-index.

	Json convert doc id key in str, must convert in int.

	:param inverted_index: inverted_index to convert
	:tyep inverted_index: dict
	:return: converted inverted-index

	"""
	new_inverted_index = dict()
	for language in inverted_index:
		new_inverted_index[language] = dict()
		for first_letter in inverted_index[language]:
			new_inverted_index[language][first_letter] = dict()
			for two_letter in inverted_index[language][first_letter]:
				new_inverted_index[language][first_letter][two_letter] = dict()
				for word in inverted_index[language][first_letter][two_letter]:
					new_inverted_index[language][first_letter][two_letter][word] = dict()
					for doc_id in inverted_index[language][first_letter][two_letter][word]:
						new_inverted_index[language][first_letter][two_letter][word][int(doc_id)] = inverted_index[language][first_letter][two_letter][word][doc_id]
	return new_inverted_index
