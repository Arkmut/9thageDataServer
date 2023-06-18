from ..utils.mongodb_router import *
import pymongo

SPELL_TYPES = ["augment", "hex", "direct", "projectile", "aura", "focused", "damage"]
SPELL_DURATIONS = ["oneTurn", "permanent", "instant"]
ITEM_TYPES = ["weapon", "armour", "banner", "artefact"]
UNIT_TYPES = ["infantry", "cavalry", "beast", "construct"]
UNIT_HEIGHTS = ["standard", "large", "gigantic"]

# armybook
if not collection_exists("ArmyBooks"):
    army_books_collection = create_collection("ArmyBooks", {
        "$jsonSchema": {
            "bsonType": "object",
            "title": "Army Book object validation",
            "required": ["name", "version", "public", "armyRules", "modelRules", "hereditarySpell", "specialItems",
                         "armyOrganisation", "armyList", "loc"],
            "properties": {
                "name": {
                    "bsonType": "string",
                    "description": "'name' must be a string and is required"
                },
                "version": {
                    "bsonType": "string",
                    "description": "'version' must be a string and is required"
                },
                "public": {
                    "bsonType": "bool",
                    "description": "'public' is required"

                },
                "armyRules": {
                    "bsonType": "object",
                    "description": "'armyRules' is required",
                    "required": ["rules"],
                    "properties": {
                        "rules": {
                            "bsonType": "array",
                            "description": "'rules' is required",
                            "items": {
                                "bsonType": "object",
                                "properties": {
                                    "name": {
                                        "bsonType": "string",
                                        "description": "'name' is required"
                                    },
                                    "definition": {
                                        "bsonType": "string",
                                        "description": "'definition' is required"
                                    },

                                }
                            }
                        }
                    }
                },
                "modelRules": {
                    "bsonType": "object",
                    "description": "'modelRules' is required",
                    "required": ["rules"],
                    "properties": {
                        "rules": {
                            "bsonType": "array",
                            "description": "'rules' is required",
                            "items": {
                                "bsonType": "object",
                                "properties": {
                                    "name": {
                                        "bsonType": "string",
                                        "description": "'name' is required"
                                    },
                                    "definition": {
                                        "bsonType": "string",
                                        "description": "'definition' is required"
                                    },

                                }
                            }
                        }
                    }

                },
                "hereditarySpell": {
                    "bsonType": "object",
                    "description": "'hereditarySpell' is required",
                    "required": ["name", "castingValue", "range", "types", "duration", "effect"],

                    "properties": {
                        "name": {
                            "bsonType": "string",
                            "description": "'name' is required"
                        },
                        "castingValue": {
                            "bsonType": "object",
                            "description": "'castingValue' is required",
                            "required": ["base"],

                            "properties": {
                                "base": {
                                    "bsonType": "number",
                                    "description": "'base' is required"
                                },
                                "boosted": {
                                    "bsonType": "number",
                                    "description": "'boosted' is required"
                                },
                            }
                        },
                        "range": {
                            "bsonType": "number",
                            "description": "'range' is required"
                        },
                        "types": {
                            "bsonType": "array",
                            "description": "'types' is required",
                            "items": {
                                "bsonType": "string",
                                "enum": SPELL_TYPES
                            }
                        },
                        "duration": {
                            "bsonType": "string",
                            "description": "'duration' is required",
                            "enum": SPELL_DURATIONS
                        },
                        "effect": {
                            "bsonType": "string",
                            "description": "'effect' is required",
                        },
                    }
                },
                "specialItems": {
                    "bsonType": "object",
                    "description": "'specialItems' is required",
                    "required": ["items"],
                    "properties": {
                        "items": {
                            "bsonType": "array",
                            "description": "'items' is required",
                            "items": {
                                "bsonType": "object",
                                "required": ["name", "type", "cost", "support", "rules"],
                                "properties": {
                                    "name": {
                                        "bsonType": "string",
                                        "description": "'name' is required"
                                    },
                                    "type": {
                                        "bsonType": "string",
                                        "description": "'type' is required",
                                        "enum": ITEM_TYPES
                                    },
                                    "cost": {
                                        "bsonType": "number",
                                        "description": "'cost' is required"
                                    },
                                    "support": {
                                        "bsonType": "array",
                                        "description": "'support' is required",
                                        "items": {
                                            "bsonType": "string",
                                        }
                                    },
                                    "maxNb": {
                                        "bsonType": "number"
                                    },
                                    "dominant": {
                                        "bsonType": "bool"
                                    },
                                    "restriction": {
                                        "bsonType": "string"
                                    },
                                    "rules": {
                                        "bsonType": "string",
                                        "description": "'rules' is required"
                                    }
                                }
                            }
                        }
                    }

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
                                    },
                                    "value": {
                                        "bsonType": "number",
                                        "description": "'value' is required"
                                    },
                                    "minimum": {
                                        "bsonType": "bool",
                                        "description": "'minimum' is required"
                                    }
                                }
                            }
                        }
                    }
                },
                "armyList": {
                    "bsonType": "object",
                    "description": "'armyList' is required",
                    "required": ["units"],
                    "properties": {
                        "units": {
                            "bsonType": "array",
                            "description": "'units' is required",
                            "items": {
                                "bsonType": "object",
                                "required": ["name", "categories", "cost", "type", "height", "baseSize",
                                             "profile"],
                                "properties": {
                                    "name": {
                                        "bsonType": "string",
                                        "description": "'name' is required"
                                    },
                                    "categories": {
                                        "bsonType": "array",
                                        "description": "'categories' is required",
                                        "items": {
                                            "bsonType": "string"
                                        }
                                    },
                                    "cost": {
                                        "bsonType": "number",
                                        "description": "'cost' is required"
                                    },
                                    "unitSize": {
                                        "bsonType": "number",
                                    },
                                    "type": {
                                        "bsonType": "string",
                                        "description": "'type' is required",
                                        "enum": UNIT_TYPES
                                    },
                                    "height": {
                                        "bsonType": "string",
                                        "description": "'height' is required",
                                        "enum": UNIT_HEIGHTS
                                    },
                                    "baseSize": {
                                        "bsonType": "object",
                                        "description": "'baseSize' is required",
                                        "required": ["width", "depth"],
                                        "properties": {
                                            "width": {
                                                "bsonType": "number",
                                                "description": "'width' is required",
                                            },
                                            "depth": {
                                                "bsonType": "number",
                                                "description": "'width' is required",
                                            },
                                        }
                                    },
                                    "profile": {
                                        "bsonType": "object",
                                        "description": "'profile' is required",
                                        "required": ["global", "defense", "offenses"],
                                        "properties": {
                                            "global": {
                                                "bsonType": "object",
                                                "description": "'global' is required",
                                                "required": ["advanceRate", "marchRate", "discipline"],
                                                "properties": {
                                                    "advanceRate": {
                                                        "bsonType": "string",
                                                        "description": "'advanceRate' is required",
                                                    },
                                                    "marchRate": {
                                                        "bsonType": "string",
                                                        "description": "'marchRate' is required",
                                                    },
                                                    "discipline": {
                                                        "bsonType": "string",
                                                        "description": "'discipline' is required",
                                                    },
                                                    "rules": {
                                                        "bsonType": "array",
                                                        "items": {
                                                            "bsonType": "string"
                                                        }
                                                    },
                                                }
                                            },
                                            "defense": {
                                                "bsonType": "object",
                                                "description": "'defense' is required",
                                                "required": ["hp", "defensiveSkill", "resistance", "armour"],
                                                "properties": {
                                                    "hp": {
                                                        "bsonType": "string",
                                                        "description": "'hp' is required",
                                                    },
                                                    "defensiveSkill": {
                                                        "bsonType": "string",
                                                        "description": "'defensiveSkill' is required",
                                                    },
                                                    "resistance": {
                                                        "bsonType": "string",
                                                        "description": "'resistance' is required",
                                                    },
                                                    "armour": {
                                                        "bsonType": "string",
                                                        "description": "'resistance' is required",
                                                    },
                                                    "rules": {
                                                        "bsonType": "array",
                                                        "items": {
                                                            "bsonType": "string"
                                                        }
                                                    },
                                                }
                                            },
                                            "offenses": {
                                                "bsonType": "array",
                                                "description": "'offenses' is required",

                                                "items": {
                                                    "bsonType": "object",
                                                    "required": ["name", "attacks", "offensiveSkill", "strength", "ap",
                                                                 "agility"],
                                                    "properties": {
                                                        "name": {
                                                            "bsonType": "string",
                                                            "description": "'name' is required",
                                                        },
                                                        "attacks": {
                                                            "bsonType": "string",
                                                            "description": "'attacks' is required",
                                                        },
                                                        "offensiveSkill": {
                                                            "bsonType": "string",
                                                            "description": "'offensiveSkill' is required",
                                                        },
                                                        "strength": {
                                                            "bsonType": "string",
                                                            "description": "'strength' is required",
                                                        },
                                                        "ap": {
                                                            "bsonType": "string",
                                                            "description": "'ap' is required",
                                                        },
                                                        "agility": {
                                                            "bsonType": "string",
                                                            "description": "'agility' is required",
                                                        },
                                                        "rules": {
                                                            "bsonType": "array",
                                                            "items": {
                                                                "bsonType": "string"
                                                            }
                                                        },
                                                    }
                                                }
                                            },

                                        }
                                    },
                                    "options": {
                                        "bsonType": "array",
                                        "items": {
                                            "oneOf": [
                                                {
                                                    "bsonType": "object",
                                                    "required": ["name", "max"],
                                                    "properties": {
                                                        "name": {
                                                            "bsonType": "string",
                                                            "description": "'name' is required"
                                                        },
                                                        "max": {
                                                            "bsonType": "number",
                                                            "description": "'max' is required"
                                                        },
                                                    }
                                                },
                                                {
                                                    "bsonType": "object",
                                                    "required": ["list", "nbChoices"],
                                                    "properties": {
                                                        "list": {
                                                            "bsonType": "array",
                                                            "description": "'list' is required",
                                                            "items": {
                                                                "bsonType": "object",
                                                                "required": ["name", "cost"],
                                                                "properties": {
                                                                    "name": {
                                                                        "bsonType": "string",
                                                                        "description": "'name' is required"
                                                                    },
                                                                    "cost": {
                                                                        "bsonType": "number",
                                                                        "description": "'cost' is required"
                                                                    },
                                                                }
                                                            }
                                                        },
                                                        "nbChoices": {
                                                            "bsonType": "number",
                                                            "description": "'nbChoices' is required"
                                                        },
                                                    }
                                                },
                                                {
                                                    "bsonType": "object",
                                                    "required": ["name", "cost"],
                                                    "properties": {
                                                        "name": {
                                                            "bsonType": "string",
                                                            "description": "'name' is required"
                                                        },
                                                        "cost": {
                                                            "bsonType": "number",
                                                            "description": "'cost' is required"
                                                        },
                                                    }
                                                },
                                                {
                                                    "bsonType": "object",
                                                    "required": ["list"],
                                                    "properties": {
                                                        "list": {
                                                            "bsonType": "array",
                                                            "description": "'list' is required",
                                                            "items": {
                                                                "bsonType": "object",
                                                                "required": ["name", "cost"],
                                                                "properties": {
                                                                    "name": {
                                                                        "bsonType": "string",
                                                                        "description": "'name' is required"
                                                                    },
                                                                    "cost": {
                                                                        "bsonType": "number",
                                                                        "description": "'cost' is required"
                                                                    },
                                                                }
                                                            }
                                                        }
                                                    }
                                                },
                                            ]
                                        }
                                    }
                                }
                            }

                        }
                    }

                },
                "loc": {
                    "bsonType": "object",
                    "required": ["en"],
                    "properties": {
                        "en": {
                            "bsonType": "object"
                        }
                    }

                }

            }
        }
    }, [("name", pymongo.ASCENDING), ("version", pymongo.DESCENDING)])


def get_armybooks(user_known: bool, public_armies: {}):
    if user_known:
        return list(get_all("ArmyBooks"))
    else:
        res = []
        for el in public_armies.keys():
            army = get_army(el, public_armies[el])
            if len(army) > 0:
                res.append(army[0])
        return res


def get_army(name: str, version: str):
    return list(get("ArmyBooks", {'name': name, 'version': version}))


def add_army(name: str, version: str):
    return bulk_add("ArmyBooks", [{
        "name": name,
        "version": version,
        "public": False,
        "armyRules": {
            "rules": []
        },
        "modelRules": {
            "rules": []
        },
        "hereditarySpell": {
            "name": "",
            "castingValue": {
                "base": 0
            },
            "range": 0,
            "types": [],
            "duration": "oneTurn",
            "effect": ""
        },
        "specialItems": {
            "items": []
        },
        "armyOrganisation": {
            "categories": []
        },
        "armyList": {
            "units": []
        },
        "loc": {
            "en": {}
        }
    }])


def army_check(army):
    return None


def save_army(name: str, version: str, army: {}):
    return update("ArmyBooks", {'name': name, 'version': version}, {'$set': army})


def delete_army(name: str, version: str):
    return delete("ArmyBooks", {'name': name, 'version': version})


RSC_PATH_BALISE = "$RSC_PATH$"
RSC_PATH = "./rsc"
ARMY_NAME_TAG_BALISE = "$ARMY_NAME_TAG$"
ARMY_NAME_BALISE = "$ARMY_NAME$"
ARMY_VERSION_BALISE = "$ARMY_VERSION$"
CURRENT_DATE_BALISE = "$CURRENT_DATE$"
ARMY_INITIALS_BALISE = "$ARMY_INITIALS$"
CHANGELOG_BALISE = "$CHANGELOG$"


def format_template(army: {}, date, date_format, template: str):
    name_tag = army['name'].replace(" ", "_").lower()
    name_initials = ""
    for el in army['name'].split(" "):
        name_initials += el.upper()[0]
    template = template.replace(RSC_PATH_BALISE, RSC_PATH)
    template = template.replace(ARMY_NAME_TAG_BALISE, name_tag)
    template = template.replace(ARMY_NAME_BALISE, army['name'])
    template = template.replace(ARMY_VERSION_BALISE, army['version'])
    template = template.replace(CURRENT_DATE_BALISE, date.strftime(date_format))
    template = template.replace(ARMY_INITIALS_BALISE, name_initials)
    # TODO changelog
    changelog = ""
    template = template.replace(CHANGELOG_BALISE, changelog)

    return template


def generate_filename(army: {}):
    return army['name'].replace(" ", "_").lower() + ".pdf"
