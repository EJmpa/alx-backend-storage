#!/usr/bin/env python3
"""
Return a list of schools having a specific topic.
"""

from pymongo.collection import Collection
from typing import List


def schools_by_topic(mongo_collection: Collection, topic: str) -> List[dict]:
    """
    Return a list of schools that have a specific topic.

    Args:
        mongo_collection (Collection): The pymongo collection object.
        topic (str): The topic to search for.

    Returns:
        list: A list of schools that have the specified topic.
    """
    schools = mongo_collection.find({"topics": topic})
    return list(schools)

