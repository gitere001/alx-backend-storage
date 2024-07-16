#!/usr/bin/env python3
""" contains a module update_topics """
import pymongo

def update_topics(mongo_collection, name, topics):
    """
    Update the 'topics' field for a document in the MongoDB collection.

    Args:
        mongo_collection (pymongo.collection.Collection): The MongoDB collection to update.
        name (str): The name of the document to update.
        topics (list): The list of topics to update in the document.

    Returns:
        None
    """

    query = {"name": name}
    new_values = {"$set": {"topics": topics}}
    mongo_collection.update_many(query, new_values)
