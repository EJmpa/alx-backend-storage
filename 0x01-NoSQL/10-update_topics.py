#!/usr/bin/env python3
"""
Update topics of a school document based on the name.
"""

from pymongo.collection import Collection


def update_topics(mongo_collection: Collection, name: str, topics: list):
    """
    Update the topics of a school document in a MongoDB collection.

    Args:
        mongo_collection (Collection): The pymongo collection object.
        name (str): The school name to update.
        topics (list of str): The list of topics to set for the school.

    Returns:
        None
    """
    # Use the update_one method to find the document with the specified name
    # and update its topics.
    mongo_collection.update_one({"name": name}, {"$set": {"topics": topics}})

