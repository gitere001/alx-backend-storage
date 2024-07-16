#!/usr/bin/env python3
"""model for the collection in the database
"""


import pymongo


def list_all(mongo_collection):
    """
    Returns all documents in a collection.

    Args:
        mongo_collection (pymongo.collection.Collection): The collection to query.

    Returns:
        list: A list of documents in the collection.
    """
    # If no collection is provided, return an empty list
    if mongo_collection is None:
        return []

    # Query the collection for all documents
    docs = mongo_collection.find()

    # Convert the cursor to a list and return it
    return [doc for doc in docs]
