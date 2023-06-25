from ..utils.mongodb_router import *
import pymongo
import re

SPELL_TYPES = ["augment", "hex", "direct", "projectile", "aura", "focused", "damage"]
SPELL_DURATIONS = ["oneTurn", "permanent", "instant"]
ITEM_TYPES = ["weapon", "armour", "banner", "artefact"]
UNIT_TYPES = ["infantry", "cavalry", "beast", "construct"]
UNIT_HEIGHTS = ["standard", "large", "gigantic"]
RULE_TYPES = ["universal", "attack_attributes/shooting", "armoury/armour",
              "armoury/shootingweapon", "armoury/closecombatweapon"]

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
                                    "type": {
                                        "bsonType": "string",
                                        "description": "'type' is required",
                                        "enum": RULE_TYPES
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
                                    "type": {
                                        "bsonType": "string",
                                        "description": "'type' is required",
                                        "enum": RULE_TYPES
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
LANGUAGE_DEF_BALISE = "$LANGUAGE_DEF$"
LANGUAGE_BALISE = "$LANGUAGE$"
LANGUAGE_DATA_BALISE = "$LANGUAGE_DATA$"
ARMY_SPECIFIC_RULES_BALISE = "$ARMY_SPECIFIC_RULES$"
MODEL_RULES_UNIVERSAL_BALISE = "$MODEL_RULES_UNIVERSAL$"
MODEL_RULES_AA_BALISE = "$MODEL_RULES_AA$"
MODEL_RULES_ARMOURY_BALISE = "$MODEL_RULES_ARMOURY$"
HE_SPELL_NAME_BALISE = "$HE_SPELL_NAME$"
HE_BASE_VALUE_BALISE = "$HE_BASE_VALUE$"
HE_BOOSTED_VALUE_BALISE = "$HE_BOOSTED_VALUE$"
HE_RANGE_BALISE = "$HE_RANGE$"
HE_TYPES_BALISE = "$HE_TYPES$"
HE_DURATION_BALISE = "$HE_DURATION$"
HE_EFFECT_BALISE = "$HE_EFFECT$"


def format_template(army: {}, date, date_format, template: str, language: str):
    name_tag = army['name'].replace(" ", "_").lower()
    language_tag = language.upper()
    name_initials = ""
    for el in army['name'].split(" "):
        name_initials += el.upper()[0]
    template = template.replace(RSC_PATH_BALISE, RSC_PATH)
    template = template.replace(ARMY_NAME_TAG_BALISE, name_tag)
    template = template.replace(ARMY_NAME_BALISE, army['name'])
    template = template.replace(ARMY_VERSION_BALISE, army['version'])
    template = template.replace(CURRENT_DATE_BALISE, date.strftime(date_format))
    template = template.replace(ARMY_INITIALS_BALISE, name_initials)
    template = template.replace(LANGUAGE_DEF_BALISE, gen_language_def(language))
    template = template.replace(LANGUAGE_BALISE, language_tag)
    template = template.replace(LANGUAGE_DATA_BALISE, gen_language_data(language, army))
    template = template.replace(ARMY_SPECIFIC_RULES_BALISE, gen_army_specific_rules(army))
    template = gen_model_rules(army, template)
    template = gen_hereditary(army, template)
    # TODO changelog
    changelog = ""
    template = template.replace(CHANGELOG_BALISE, changelog)

    return template


def gen_language_def(language):
    # TODO switch with language
    return "\\def\\languageisenglish{}"


def gen_language_data(language: str, army: {}):
    loc_table = army['loc'][language]
    res = ""
    for el in loc_table.keys():
        params = ""
        if "#" in loc_table[el]:
            paramsInText = re.findall(r"#([0-9]+)", loc_table[el])
            paramsInt = [int(el) for el in paramsInText]
            params = "[" + str(max(paramsInt)) + "]"
        res += "\\newcommand{" + el + "}" + params + "{" + loc_table[el] + "}\n"
    return res


def generate_filename(army: {}):
    return army['name'].replace(" ", "_").lower() + ".pdf"


def gen_army_specific_rules(army: {}):
    res = ""
    for el in army['armyRules']['rules']:
        res += "\\AMRsortedlistentry{" + el['name'] + "{}}{" + el['definition'] + "}\n"
    return res


def gen_model_rules(army: {}, template: str):
    rules = [rule for rule in army['modelRules']['rules'] if rule['type'] == "universal"]
    template = template.replace(MODEL_RULES_UNIVERSAL_BALISE,
                                gen_model_rules_internal(rules, "\\universalrules", ""))

    rules = [rule for rule in army['modelRules']['rules'] if "attack_attributes" in rule['type']]
    template = template.replace(MODEL_RULES_AA_BALISE,
                                gen_model_rules_internal(rules, "\\attackattributes", ["shooting"]))

    rules = [rule for rule in army['modelRules']['rules'] if "armoury" in rule['type']]
    template = template.replace(MODEL_RULES_ARMOURY_BALISE,
                                gen_model_rules_internal(rules, "\\armoury",
                                                         ["armour", "shootingweapon", "closecombatweapon"]))

    return template


def gen_model_rules_internal(rule_list: [], subtitle: str, subtypes: [str]):
    res = "\\subtitle{" + subtitle + "}\n"
    if len(subtypes) > 0:
        for st in subtypes:
            subtype_str = "[\\" + st + "]"
            res += "\\startAMRsortedlist\n"
            sublist = [r for r in rule_list if st in r['type']]
            for el in sublist:
                res += "\\AMRsortedlistentry" + subtype_str + "{" + el['name'] + "{}}{" + el['definition'] + "}\n"
            res += "\\closeAMRsortedlist\n"

    else:
        res += "\\startAMRsortedlist\n"
        for el in rule_list:
            res += "\\AMRsortedlistentry{" + el['name'] + "{}}{" + el['definition'] + "}\n"
        res += "\\closeAMRsortedlist\n"
    return res


def gen_spell_type(el:str):
    return "\\"+el.lower()


def gen_spell_duration(param:str):
    return "\\"+param.lower()


def gen_hereditary(army: {}, template: str):
    template = template.replace(HE_SPELL_NAME_BALISE, army['hereditarySpell']['name'])
    template = template.replace(HE_BASE_VALUE_BALISE, str(army['hereditarySpell']['castingValue']['base'])+"+")
    if 'boosted' in army['hereditarySpell']['castingValue']:
        template = template.replace(HE_BOOSTED_VALUE_BALISE,  str(army['hereditarySpell']['castingValue']['boosted'])+"+")
    else:
        template = template.replace(HE_BOOSTED_VALUE_BALISE, "")
    template = template.replace(HE_RANGE_BALISE,  str(army['hereditarySpell']['range']))
    types = ""
    for el in army['hereditarySpell']['types']:
        types += "\\HStype{" + gen_spell_type(el) + "}\n"
    template = template.replace(HE_TYPES_BALISE, types)
    template = template.replace(HE_DURATION_BALISE, gen_spell_duration(army['hereditarySpell']['duration']))
    template = template.replace(HE_EFFECT_BALISE, army['hereditarySpell']['effect'])

    return template


def parse_translation(latex: str):
    data = {}
    lines = latex.split('\n')
    lines = [l for l in lines if l not in ["\n"]]
    searchingClosingBrace = False
    currentTranslation = ""
    currentValue = ""
    openingBraceCounter = 0
    closingBraceCounter = 0
    for l in lines:
        if not searchingClosingBrace:
            newcommand_tag = "\\newcommand{"
            if newcommand_tag not in l:
                continue
            currentTranslation = l[l.index(newcommand_tag) + len(newcommand_tag):l.index("}")]
            l = l[l.index("}") + 1:]
            openingBraceCounter = l.count('{')
            closingBraceCounter = l.count('}')
            if openingBraceCounter > closingBraceCounter:
                searchingClosingBrace = True
                currentValue += "\n" + l[l.index('{') + 1:]
            else:
                data[currentTranslation] = l[l.index('{') + 1:l.rindex("}")]
        else:
            openingBraceCounter += l.count('{')
            closingBraceCounter += l.count('}')
            if openingBraceCounter > closingBraceCounter:
                searchingClosingBrace = True
                currentValue += "\n" + l
            else:
                currentValue += "\n" + l[0:l.rindex("}")]
                data[currentTranslation] = currentValue
                currentValue = ""
                currentTranslation = ""
                searchingClosingBrace = False
                openingBraceCounter = 0
                closingBraceCounter = 0

    return data
