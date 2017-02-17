#!/usr/bin/python3

import re
import gzip
import sys
import os
import urllib.request
import io
import json
import shutil
from pymongo import MongoClient

files = os.listdir()

for i in range(0, len(files)):
	files[i] = os.path.join(os.getcwd(), files[i])

archive_url = "http://data.githubarchive.org/"

def downloadFile(f):
	print ("URL: {}".format(archive_url + f))
	res = urllib.request.urlopen(archive_url + f)
	compressed_file = io.BytesIO(res.read())
	archive_file = open(f, 'wb')
	shutil.copyfileobj(compressed_file, archive_file)
	archive_file.close()

def decompressAndSaveToMongo(f):
	fileobj = open(f, 'rb')

	# read the file
	flie = gzip.GzipFile(fileobj=fileobj)
	fl = io.StringIO(flie.read().decode('utf-8'))
	lines = fl.readlines()
	fl.close()
	
	# convert the strings into json
	data = []
	for line in lines:
		data.append(json.loads(line))

	# save the data into mongo collection events
	events.insert_many(data)

client = MongoClient()
db = client.github_events
events = db.events

prefix = '2016-01-01-'

for hour in range(0, 24):
	print("Downloading file: {}".format(prefix + str(hour) + '.json.gz'))
	downloadFile(prefix + str(hour) + '.json.gz')
	print("Saving file: {}".format(prefix + str(hour) + '.json'))
	decompressAndSaveToMongo(prefix + str(hour) + '.json.gz')


