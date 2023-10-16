#!/usr/bin/env python3
"""
Inserts a new document into a collection based on kwargs.
"""
from pymongo.collection import Collection


def insert_school(mongo_collection: Collection, **kwargs) -> str:
    """
    Inserts a new document into the collection based on kwargs.

    Args:
        mongo_collection (pymongo.collection.Collection): The collection to
        insert the document into.
        **kwargs: Keyword arguments to define the document.

    Returns:
        str: The _id of the newly inserted document.
    """
    new_school = kwargs
    result = mongo_collection.insert_one(new_school)
    return str(result.inserted_id)
