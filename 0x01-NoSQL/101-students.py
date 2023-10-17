#!/usr/bin/env python3
"""
101-students
"""

from pymongo import MongoClient
from typing import List, Dict, Any


def top_students(mongo_collection: Any) -> List[Dict[str, Any]]:
    """
    Returns all students sorted by average score.
    
    :param mongo_collection: pymongo collection object
    :return: List of students sorted by average score
    """
    pipeline = [
        {
            '$project': {
                'name': 1,
                'topics': 1,
                'averageScore': {
                    '$avg': '$topics.score'
                }
            }
        },
        {
            '$sort': {
                'averageScore': -1
            }
        }
    ]

    top_students = list(mongo_collection.aggregate(pipeline))
    return top_students
