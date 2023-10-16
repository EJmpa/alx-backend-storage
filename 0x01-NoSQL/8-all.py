#!/usr/bin/env python3
"""
Lists all documents in a collection.
"""
from pymongo.collection import Collection
from typing import List


def list_all(mongo_collection: Collection) -> List[dict]:
    """
    Lists all documents in the given collection.

    Args:
        mongo_collection (pymongo.collection.Collection): The collection
        to list documents from.

    Returns:
        list: A list of documents as dictionaries.
    """
    documents = list(mongo_collection.find({}))
    return documents
