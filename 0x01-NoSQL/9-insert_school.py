#!/usr/bin/env python3
""" inserts a new document in a collection """


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a collection.

    Args:
        mongo_collection (pymongo.collection.Collection): The collection to insert the document into.
        **kwargs: The document to insert.

    Returns:
        objectid.ObjectId: The ObjectId of the inserted document.
    """
    # Insert the document into the collection and return the ObjectId of the inserted document
    insert_result = mongo_collection.insert_one(kwargs)
    return insert_result.inserted_id
