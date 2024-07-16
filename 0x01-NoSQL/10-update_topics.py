#!/usr/bin/env python3

import pymongo

def update_topics(mongo_collection, name, topics):
	"""
	Updates all topics of a school document based on the name.

	Args:
		mongo_collection (pymongo.collection.Collection): The collection to update.
		name (str): The name of the school document.
		topics (list): The list of topics to update.

	Returns:
		int: The number of modified documents.
	"""
	# Update all documents in the collection based on the name
	result = mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})

	# Return the number of modified documents
	return result
