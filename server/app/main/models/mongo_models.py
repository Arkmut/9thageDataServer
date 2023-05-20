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
    }, [pymongo.IndexModel([("name", pymongo.ASCENDING)]), pymongo.IndexModel([("version", pymongo.DESCENDING)])])


def get_armybooks():
    return get_all("ArmyBooks")


def get_army(name: str, version: str):
    return get("ArmyBooks", {'name': name, 'version': version})


def add_army(name: str, version: str):
    return bulk_add("ArmyBooks", [{
        "name": name,
        "version": version
    }])
