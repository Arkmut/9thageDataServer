from ..utils.mongodb_router import *
import pymongo

# armybook
if not collection_exists("ArmyBooks"):
    army_books_collection = create_collection("ArmyBooks", {
        "$jsonSchema": {
            "bsonType": "object",
            "title": "Army Book object validation",
            "required": ["name", "version", "armyRules", "modelRules", "hereditarySpell", "specialItems",
                         "armyOrganisation", "units"],
            "properties": {
                "name": {
                    "bsonType": "string",
                    "description": "'name' must be a string and is required"
                },
                "version": {
                    "bsonType": "string",
                    "description": "'version' must be a string and is required"
                },
                "armyRules": {
                    "bsonType": "object",
                    "description": "'armyRules' is required"
                },
                "modelRules": {
                    "bsonType": "object",
                    "description": "'modelRules' is required"
                },
                "hereditarySpell": {
                    "bsonType": "object",
                    "description": "'hereditarySpell' is required"
                },
                "specialItems": {
                    "bsonType": "object",
                    "description": "'specialItems' is required"
                },
                "armyOrganisation": {
                    "bsonType": "object",
                    "description": "'armyOrganisation' is required",
                    "properties": {

                        "categories": {
                            "bsonType": "array",
                            "description": "'categories' is required",
                            "items": {
                                "bsonType": "object",
                                "properties": {

                                    "name": {
                                        "bsonType": "string",
                                        "description": "'name' is required"
                                    }
                                }
                            }
                        }
                    }
                },
                "units": {
                    "bsonType": "object",
                    "description": "'units' is required"
                },

            }
        }
    }, [("name", pymongo.ASCENDING), ("version", pymongo.DESCENDING)])


def get_armybooks():
    return list(get_all("ArmyBooks"))


def get_army(name: str, version: str):
    return get("ArmyBooks", {'name': name, 'version': version})


def add_army(name: str, version: str):
    return bulk_add("ArmyBooks", [{
        "name": name,
        "version": version
    }])
