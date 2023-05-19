from ..utils.mongodb_router import *
import pymongo

# armybook
if not collection_exists("ArmyBooks"):
    army_books_collection = create_collection("ArmyBooks", {
        "$jsonSchema": {
            "bsonType": "object",
            "title": "Army Book object validation",
            "required": ["name", "version"],
            "properties": {
                "name": {
                    "bsonType": "string",
                    "description": "'name' must be a string and is required"
                }, "version": {
                    "bsonType": "string",
                    "description": "'version' must be a string and is required"
                }
            }
        }
    }, [("name", pymongo.ASCENDING), ("version", pymongo.DESCENDING)])

def get_armybooks():
    return get_all("ArmyBooks")
