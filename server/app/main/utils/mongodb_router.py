import logging

import pymongo
import os

client = pymongo.MongoClient(host=os.environ.get('MONGO_DB_HOST'), port=int(os.environ.get('MONGO_DB_PORT')),
                             username=os.environ.get('MONGO_DB_USERNAME'), password=os.environ.get('MONGO_DB_PASSWORD'))
db_handle = client[os.environ.get('MONGO_DB_NAME')]
logger_router = logging.getLogger(__name__)


def bulk_add(collection: str, elements: [dict]):
    db_handle[collection].insert_many(elements)


def add_one(collection: str, element: {}):
    db_handle[collection].insert_one(element)


def get_all(collection: str):
    return db_handle[collection].find()


def get(collection: str, dict_index: dict):
    return db_handle[collection].find(dict_index)


def update(collection: str, dict_index: dict, object: dict):
    old_id = get(collection,dict_index)[0]['_id']
    object['_id']=old_id
    return db_handle[collection].replace_one(dict_index, object)


def delete(collection: str, dict_index: dict):
    return db_handle[collection].delete_one(dict_index)


def create_collection(collection: str, schema: dict, indexes: [tuple]):
    db_handle.create_collection(collection, validator=schema)
    db_handle[collection].create_index(indexes, unique=True)
    return db_handle[collection]


def transaction_update(collection, schema, indexes):
    all_data = list(get_all(collection))
    logger_router.info(f"old data: {all_data}")
    # we drop the collection
    db_handle[collection].drop()

    # we recreate it with all data
    create_collection(collection, schema, indexes)
    for data in all_data:
        add_one(collection, data)


def update_schema(collection: str, schema: dict, indexes: [tuple]):
    logger_router.info(f"old data: {list(get_all(collection))}")
    with client.start_session() as session:
        # Step 3: Use with_transaction to start a transaction, execute the callback, and commit (or abort on error).
        session.with_transaction(
            lambda s: transaction_update(collection, schema, indexes),
            read_concern=pymongo.read_concern.ReadConcern("local"),
            read_preference=pymongo.ReadPreference.PRIMARY,
        )
    logger_router.info(f"new data: {list(get_all(collection))}")


def collection_exists(collection: str) -> bool:
    try:
        db_handle.validate_collection(collection)  # Try to validate a collection
        return True
    except pymongo.errors.OperationFailure:  # If the collection doesn't exist
        return False
