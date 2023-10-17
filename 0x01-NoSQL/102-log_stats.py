#!/usr/bin/env python3
"""
Provides stats about Nginx logs stored in MongoDB.
"""

from pymongo import MongoClient
from pymongo.collection import Collection


def log_stats(mongo_collection: Collection) -> None:
    """
    Displays statistics about Nginx logs.

    Args:
        mongo_collection (pymongo.collection.Collection): The
        collection to retrieve data from.
    """
    total_logs = mongo_collection.count_documents({})

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = (
            {method: mongo_collection.count_documents(
                {"method": method}) for method in methods}
            )

    status_check = mongo_collection.count_documents(
            {"method": "GET", "path": "/status"}
            )

    print(f"{total_logs} logs")
    print("Methods:")
    for method, count in method_counts.items():
        print(f"\tmethod {method}: {count}")

    ips_pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]

    top_ips = list(mongo_collection.aggregate(ips_pipeline))

    print(f"{status_check} status check")
    print("IPs:")
    for entry in top_ips:
        ip, count = entry["_id"], entry["count"]
        print(f"\t{ip}: {count}")


if __name__ == "__main__":

    client = MongoClient('mongodb://127.0.0.1:27017')
    mongo_db = client.logs
    mongo_collection = mongo_db.nginx
    log_stats(mongo_collection)
