#!/usr/bin/python
# script for separating the repositories from the github events

import os
from github_events import handler
from pymongo import MongoClient
import pprint

client = MongoClient()
events = client["github_events"].events

repos = dict()
users = dict()

store = {
	'users': users,
	'repos': repos
}

print("{} documents to be scanned".format(events.count()))
count = events.find({ 'type': 'CommitCommentEvent'}).count()
print("{} events with CommitCommentEvent".format(count))

for event in events.find():
	if handler.get(event['type']) != None:
		handler[event['type']](event, store)

print("{} users found".format(len(store['users'].keys())))
print("{} repos found".format(len(store['repos'].keys())))

