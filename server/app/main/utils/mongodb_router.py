import logging

import pymongo
import os

db_handle = pymongo.MongoClient(host=os.environ.get('MONGO_DB_HOST'), port=int(os.environ.get('MONGO_DB_PORT')),
                                username=os.environ.get('MONGO_DB_USERNAME'),
                                password=os.environ.get('MONGO_DB_PASSWORD'))[os.environ.get('MONGO_DB_NAME')]
logger_router = logging.getLogger(__name__)


def bulk_add(collection: str, elements: [dict]):
    db_handle[collection].insert_many(elements)


def get_all(collection: str):
    return db_handle[collection].find()


def get(collection: str, dict_index: dict):
    return db_handle[collection].find(dict_index)


def create_collection(collection: str, schema: dict, indexes: [tuple]):
    db_handle.create_collection(collection, validator=schema)
    db_handle[collection].create_index(indexes,unique=True)
    return db_handle[collection]


def collection_exists(collection: str) -> bool:
    try:
        db_handle.validate_collection(collection)  # Try to validate a collection
        return True
    except pymongo.errors.OperationFailure:  # If the collection doesn't exist
        return False
