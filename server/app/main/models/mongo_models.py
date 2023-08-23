from ..utils.mongodb_router import *
import pymongo
import re

SPELL_TYPES = ["augment", "hex", "direct", "projectile", "aura", "focused", "damage"]
SPELL_DURATIONS = ["oneTurn", "permanent", "instant"]
ITEM_TYPES = ["weapon", "armour", "banner", "artefact", "kindred", "aspectsofnature"]
UNIT_TYPES = ["infantry", "cavalry", "beast", "construct"]
UNIT_HEIGHTS = ["standard", "large", "gigantic"]
RULE_TYPES = ["universal", "attack_attributes/shooting", "attack_attributes/closecombat", "armoury/armour",
              "armoury/shootingweapon",
              "armoury/closecombatweapon", "armoury/artilleryweapon", "special_attacks"]
ARMYBOOK_SCHEMA = {
    "bsonType": "object",
    "title": "Army Book object validation",
    "required": ["name", "version", "public", "armyRules", "modelRules", "specialItems",
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
                        "required": ["name", "logo", "value", "minimum"],
                        "properties": {

                            "name": {
                                "bsonType": "string",
                                "description": "'name' is required"
                            },
                            "logo": {
                                "bsonType": "string",
                                "description": "'logo' is required"
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
                            "fluff": {
                                "bsonType": "string",
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
                            "maxunitsize": {
                                "bsonType": "number",
                            },
                            "costpermodel": {
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
                                                    "bsonType": "object",
                                                    "required": ['name', 'equipment'],
                                                    "properties": {
                                                        "name": {
                                                            "bsonType": "string",
                                                            "description": "'name' is required",
                                                        },
                                                        "equipment": {
                                                            "bsonType": "bool",
                                                            "description": "'equipment' is required",
                                                        },
                                                    }
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
                                                    "bsonType": "object",
                                                    "required": ['name', 'equipment'],
                                                    "properties": {
                                                        "name": {
                                                            "bsonType": "string",
                                                            "description": "'name' is required",
                                                        },
                                                        "equipment": {
                                                            "bsonType": "bool",
                                                            "description": "'equipment' is required",
                                                        },
                                                    }
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
                                                        "bsonType": "object",
                                                        "required": ['name', 'equipment'],
                                                        "properties": {
                                                            "name": {
                                                                "bsonType": "string",
                                                                "description": "'name' is required",
                                                            },
                                                            "equipment": {
                                                                "bsonType": "bool",
                                                                "description": "'equipment' is required",
                                                            },
                                                        }
                                                    }
                                                },
                                            }
                                        }
                                    },

                                }
                            },
                            "restrictions": {
                                "bsonType": "object",
                                "properties": {
                                    "maxPerArmy": {
                                        "bsonType": "number"
                                    },
                                    "maxModelsPerArmy": {
                                        "bsonType": "number"
                                    },
                                    "sharedMaxPerArmy": {
                                        "bsonType": "number"
                                    },
                                    "specialNote": {
                                        "bsonType": "string"
                                    },

                                }
                            },
                            "categoryChange": {
                                "bsonType": "object",
                                "required": ["condition"],
                                "properties": {
                                    "condition": {
                                        "bsonType": "string"
                                    }
                                }
                            },
                            "options": {
                                "bsonType": "array",
                                "items": {

                                    "bsonType": "object",
                                    "required": ["globalName", "globalPrice", "values"],
                                    "properties": {
                                        "globalName": {
                                            "bsonType": "string",
                                            "description": "'globalName' is required"
                                        },
                                        "globalPrice": {
                                            "bsonType": "string",
                                            "description": "'globalPrice' is required"
                                        },
                                        "values": {
                                            "bsonType": "array",
                                            "description": "'values' is required",
                                            "items": {
                                                "bsonType": "object",
                                                "required": ['name', 'price'],
                                                "properties": {
                                                    "name": {
                                                        "bsonType": "string",
                                                        "description": "'name' is required"
                                                    },
                                                    "price": {
                                                        "bsonType": "string",
                                                        "description": "'price' is required"
                                                    },
                                                }
                                            }
                                        },
                                        "isMount": {
                                            "bsonType": "bool"

                                        },
                                        "isMagic": {
                                            "bsonType": "bool"

                                        },
                                        "isCommandGroup": {
                                            "bsonType": "bool"

                                        },
                                    }

                                }
                            },
                            "paths": {
                                "bsonType": "array",
                                "items": {
                                    "bsonType": "string"
                                }
                            },
                            "modelRules": {
                                "bsonType": "array",
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

                        },

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

# armybook
if not collection_exists("ArmyBooks"):
    army_books_collection = create_collection("ArmyBooks", {"$jsonSchema": ARMYBOOK_SCHEMA},
                                              [("name", pymongo.ASCENDING), ("version", pymongo.DESCENDING)])
else:
    update_schema("ArmyBooks", {"$jsonSchema": ARMYBOOK_SCHEMA},
                  [("name", pymongo.ASCENDING), ("version", pymongo.DESCENDING)])


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
    logger_router.info(f"mongo request: {name} {version}")
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
    return replace("ArmyBooks", {'name': name, 'version': version}, army)


def edit_army_name(oldName: str, oldVersion: str, version: str, name: str):
    return update("ArmyBooks", {'name': oldName, 'version': oldVersion}, {'name': name, 'version': version})


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
MODEL_RULES_SA_BALISE = "$MODEL_RULES_SA$"
MODEL_RULES_ARMOURY_BALISE = "$MODEL_RULES_ARMOURY$"
HE_SPELL_NAME_BALISE = "$HE_SPELL_NAME$"
HE_BASE_VALUE_BALISE = "$HE_BASE_VALUE$"
HE_BOOSTED_VALUE_BALISE = "$HE_BOOSTED_VALUE$"
HE_RANGE_BALISE = "$HE_RANGE$"
HE_TYPES_BALISE = "$HE_TYPES$"
HE_DURATION_BALISE = "$HE_DURATION$"
HE_EFFECT_BALISE = "$HE_EFFECT$"
SPECIAL_EQUIPEMENT_BALISE_START = "$SPECIAL_EQUIPMENT_"
SPECIAL_EQUIPEMENT_BALISE_END = "$"
ARMY_ORG_NB_BALISE = "$ARMY_ORG_NB$"
ARMY_ORG_DATA_BALISE = "$ARMY_ORG_DATA$"
ARMY_LIST_BALISE = "$ARMY_LIST$"
QRS_SHOOTING_WEAPONS_BALISE = "$QRS_SHOOTING_WEAPONS$"
QRS_AIM_TABLE_BALISE = "$QRS_AIM_TABLE$"
TOC_PART1_BALISE = "$TOC_PART1$"
TOC_PART2_BALISE = "$TOC_PART2$"
FOOTER_PART1_BALISE = "$FOOTER_PART1$"
FOOTER_PART2_BALISE = "$FOOTER_PART2$"


def gen_army_name(army):
    return army['name'].lower().replace("\\newline", "").replace("\\", "").replace(" ", "_").replace("__", "_").replace(
        ":", "").replace(",", "")


def gen_toc(army: {}, template: str, changelog: str):
    part1 = ""
    if len(army['armyRules']['rules']) > 0:
        part1 += "\t\\tocentry{ArmySpecificRules}{\\armyspecificrules}\\par\n"
    if len(army['modelRules']['rules']) > 0:
        part1 += "\t\\tocentry{ModelRules}{\\armymodelrules}\\par\n"
    if 'hereditarySpell' in army:
        part1 += "\t\\tocentry{HereditarySpell}{\\hereditaryspell}\\par\n"
    if len(army['specialItems']['items']) > 0:
        part1 += "\t\\tocentry{SpecialEquipment}{\\specialequipment}\\par\n"
    if len(army['armyOrganisation']['categories']) > 0:
        part1 += "\t\\tocentry{ArmyOrganisation}{\\armyorganisation}\\par\n"
    if len(army['armyList']['units']) > 0:
        part1 += "\t\\tocentry{QRS}{\\quickrefsheet}\\par\n"
    if len(changelog) > 0:
        part1 += "\t\\tocentry{changelog}{\\changelog}\\par\n"
    template = template.replace(TOC_PART1_BALISE, part1)
    part2 = ""
    for i in range(0, len(army['armyOrganisation']['categories'])):
        c = army['armyOrganisation']['categories'][i]
        nameCat = c['name'].replace('\\', '').replace('{}', '')
        part2 += f"\t\\tocentry{{{nameCat}}}{{{c['name']}}}"
        if i < len(army['armyOrganisation']['categories']) - 1:
            part2 += "\\par\n"
        else:
            part2 += "\n"
    template = template.replace(TOC_PART2_BALISE, part2)
    return template


def gen_footer(army: {}, template: str):
    part1 = ""
    if len(army['armyRules']['rules']) > 0:
        part1 += "\t\\hyperlink{ArmySpecificRules}{\\armyspecificrulesInitial}\\standardfooterspace{}%\n"
    if len(army['modelRules']['rules']) > 0:
        part1 += "\t\\hyperlink{ModelRules}{\\armymodelrulesInitial}\\standardfooterspace{}%\n"
    if 'hereditarySpell' in army:
        part1 += "\t\\hyperlink{HereditarySpell}{\\hereditaryspellInitial}\\standardfooterspace{}%\n"
    if len(army['specialItems']['items']) > 0:
        part1 += "\t\\hyperlink{SpecialEquipment}{\\specialequipmentInitial}\\standardfooterspace{}%\n"
    if len(army['armyOrganisation']['categories']) > 0:
        part1 += "\t\\hyperlink{ArmyOrganisation}{\\armyorganisationInitial}\\standardfooterspace{}%\n"
    if len(army['armyList']['units']) > 0:
        part1 += "\t\\hyperlink{QRS}{\\quickrefsheetInitial}%\n"

    template = template.replace(FOOTER_PART1_BALISE, part1)
    part2 = ""
    for c in army['armyOrganisation']['categories']:
        nameCat = c['name'].replace('\\', '').replace('{}', '')
        if 'special' in nameCat:
            part2 += f"\t\\hyperlink{{{nameCat}}}{{\\specialInitial}}\\standardfooterspace{{}}%\n"
        else:
            part2 += f"\t\\hyperlink{{{nameCat}}}{{{c['name']}Initial}}\\standardfooterspace{{}}%\n"
            if 'character' in nameCat:
                part2 += f"\t\\hyperlink{{charactermounts}}{{\\charactermountsInitial}}\\standardfooterspace{{}}%\n"

    template = template.replace(FOOTER_PART2_BALISE, part2)
    return template


def gen_army_name_initials(army):
    name_tag = gen_army_name(army)
    name_initials = ""
    for el in name_tag.split("_"):
        if len(el) == 0:
            continue
        name_initials += el.upper()[0]
    return name_initials


def format_template(army: {}, date, date_format, template: str, language: str, global_language: {}):
    name_tag = gen_army_name(army)
    language_tag = language.upper()
    name_initials = gen_army_name_initials(army)
    template = template.replace(RSC_PATH_BALISE, RSC_PATH)
    template = template.replace(ARMY_NAME_TAG_BALISE, name_tag)
    template = template.replace(ARMY_NAME_BALISE, army['name'])
    template = template.replace(ARMY_VERSION_BALISE, army['version'])
    template = template.replace(CURRENT_DATE_BALISE, date.strftime(date_format))
    template = template.replace(ARMY_INITIALS_BALISE, name_initials)
    template = template.replace(LANGUAGE_DEF_BALISE, gen_language_def(language))
    template = template.replace(LANGUAGE_BALISE, language_tag)
    template = template.replace(LANGUAGE_DATA_BALISE, gen_language_data(language, army, global_language))
    template = template.replace(ARMY_SPECIFIC_RULES_BALISE, gen_army_specific_rules(army))
    template = gen_model_rules(army, template)
    template = gen_hereditary(army, template)
    template = gen_specialitems(army, template)
    template = gen_army_organisation(army, template)
    template = gen_army_list(army, template)
    template = gen_qrs(army, template)
    # TODO changelog
    changelog = ""
    template = template.replace(CHANGELOG_BALISE, changelog)
    template = gen_toc(army, template, changelog)
    template = gen_footer(army, template)

    return template


def gen_language_def(language):
    # TODO switch with language
    return "\\def\\languageisenglish{}"


def gen_language_data(language: str, army: {}, global_language_data: {}):
    loc_table = army['loc'][language]
    logger_router.info(f"languages glob: {global_language_data.keys()}, lan: {language}")
    if language in global_language_data:
        for key, el in global_language_data[language].items():
            loc_table[key] = el
    res = ""
    for el in loc_table.keys():
        params = ""
        if "#" in loc_table[el]:
            paramsInText = re.findall(r"#([0-9]+)", loc_table[el])
            paramsInt = [int(el) for el in paramsInText]
            params = "[" + str(max(paramsInt)) + "]"
        value = ""
        # we clean all comments
        for line in loc_table[el].split('\n'):
            if '%' in line:
                value += line[0:line.index('%')] + "%\n"
            else:
                value += line + "%\n"
        res += "\\newcommand{" + el + "}" + params + "{%\n" + value + "%\n}\n"
    return res


def generate_filename(army: {}, language: str):
    return f"T9A-FB_2ed_{gen_army_name_initials(army)}_{army['version'].replace(' ', '_')}_{language.upper()}.pdf"


def gen_army_specific_rules(army: {}):
    res = ""
    for el in army['armyRules']['rules']:
        res += "\\AMRsortedlistentry{" + el['name'] + "{}}{" + el['definition'] + "}\n"
    return res


def gen_model_rules(army: {}, template: str):
    rules = [rule for rule in army['modelRules']['rules'] if rule['type'] == "universal"]
    template = template.replace(MODEL_RULES_UNIVERSAL_BALISE,
                                gen_model_rules_internal(rules, "\\universalrules", ""))
    rules = [rule for rule in army['modelRules']['rules'] if rule['type'] == "special_attacks"]
    logger_router.info(f"special attacks: {rules} in {army['modelRules']['rules']}")
    template = template.replace(MODEL_RULES_SA_BALISE,
                                gen_model_rules_internal(rules, "\\specialattacks", ""))

    rules = [rule for rule in army['modelRules']['rules'] if "attack_attributes" in rule['type']]
    template = template.replace(MODEL_RULES_AA_BALISE,
                                gen_model_rules_internal(rules, "\\attackattributes", ["attack_attributes/shooting"]))

    rules = [rule for rule in army['modelRules']['rules'] if "armoury" in rule['type']]
    template = template.replace(MODEL_RULES_ARMOURY_BALISE,
                                gen_model_rules_internal(rules, "\\armoury",
                                                         ["armoury/armour", "armoury/shootingweapon",
                                                          "armoury/closecombatweapon", "armoury/artilleryweapon"]))

    return template


def gen_model_rules_internal(rule_list: [], subtitle: str, subtypes: [str]):
    if len(rule_list) == 0:
        return ""
    res = "\\subtitle{" + subtitle + "}\n"
    if len(subtypes) > 0:
        for st in subtypes:
            subtype_str = "[" + gen_rule_type(st) + "]"
            sublist = [r for r in rule_list if st == r['type']]
            if len(sublist) == 0:
                continue
            res += "\\startAMRsortedlist\n"
            logger_router.info(f"rule subtype: {st}, list: {sublist}")
            for el in sublist:
                res += "\\AMRsortedlistentry" + subtype_str + "{" + el['name'] + "{}}{" + el['definition'] + "}\n"
            res += "\\closeAMRsortedlist\n"

    else:
        if len(rule_list) == 0:
            return ""
        res += "\\startAMRsortedlist\n"
        for el in rule_list:
            res += "\\AMRsortedlistentry{" + el['name'] + "{}}{" + el['definition'] + "}\n"
        res += "\\closeAMRsortedlist\n"
    return res


def gen_rule_type(el: str, inUnit: bool = False):
    if "attack_attributes" in el:
        return "\\attackattribute" + el.lower()[el.index("/") + 1 if ("/" in el) else 0:]
    elif "special_attacks" in el:
        return "\\specialattack"
    elif "universal" in el and inUnit:
        return "\\universalrule"
    else:
        return "\\" + el.lower()[el.index("/") + 1 if ("/" in el) else 0:]


def gen_spell_type(el: str):
    return "\\" + el.lower()


def gen_spell_duration(param: str):
    return "\\" + param.lower()


def gen_hereditary(army: {}, template: str):
    if 'hereditarySpell' not in army:
        return template
    template = template.replace(HE_SPELL_NAME_BALISE, army['hereditarySpell']['name'])
    template = template.replace(HE_BASE_VALUE_BALISE, str(army['hereditarySpell']['castingValue']['base']) + "+")
    if 'boosted' in army['hereditarySpell']['castingValue']:
        template = template.replace(HE_BOOSTED_VALUE_BALISE,
                                    str(army['hereditarySpell']['castingValue']['boosted']) + "+")
    else:
        template = template.replace(HE_BOOSTED_VALUE_BALISE, "")
    template = template.replace(HE_RANGE_BALISE, str(army['hereditarySpell']['range']))
    types = ""
    for el in army['hereditarySpell']['types']:
        types += "\\HStype{" + gen_spell_type(el) + "}\n"
    template = template.replace(HE_TYPES_BALISE, types)
    template = template.replace(HE_DURATION_BALISE, gen_spell_duration(army['hereditarySpell']['duration']))
    template = template.replace(HE_EFFECT_BALISE, army['hereditarySpell']['effect'])

    return template


def gen_specialitems_type(listItems: [{}]):
    res = "\\startsortedpricelist\n"
    for item in listItems:
        support = ""
        for i in range(0, len(item["support"])):
            support += item['support'][i] + "{}"
            if i != len(item['support']) - 1:
                support += ", "
        cost = item['cost'] if item['cost'] > 0 else ""
        enchantment = support
        maxNb = item['maxNb'] if item['maxNb'] > 1 else ""
        dominant = item['dominant'] if item['dominant'] else ""
        restriction = item['restriction'] + "{}" if len(item['restriction']) > 0 else ""
        rules = item['rules'] + "{}" if len(item['rules']) > 0 else ""
        logger_router.info(f"item: {item['type']} {item['name']}")
        res += f"\\itementry{{\ntype= {item['type']},\nname= {item['name']}{{}},\ncost= {cost},\nenchantment={enchantment},\n" \
               f"maxnumber={maxNb},\ndominant={dominant},\nrestriction= {restriction},\n" \
               f"rules= {rules},\n}}\n"
    res += "\\endsortedpricelist\n"
    return res


def gen_specialitems(army: {}, template: str):
    for type in ITEM_TYPES:
        listItems = []
        balise = SPECIAL_EQUIPEMENT_BALISE_START + type.upper() + SPECIAL_EQUIPEMENT_BALISE_END
        for item in army['specialItems']['items']:
            if item['type'] == type:
                listItems.append(item)
        logger_router.info(f"balise: {balise}")
        logger_router.info(f"nb balise: {template.count(balise)}")
        template = template.replace(balise, gen_specialitems_type(listItems))

    return template


def gen_army_organisation(army: {}, template: str):
    categories_ = army['armyOrganisation']['categories']
    template = template.replace(ARMY_ORG_NB_BALISE, str(len(categories_)))
    orgData = ""
    # logos
    for i in range(0, len(categories_)):
        ao = categories_[i]
        orgData += "\\armyorganizationlogo{" + ao['logo'] + "}"
        if i < len(categories_) - 1:
            orgData += "&\n"
        else:
            orgData += "\\tabularnewline\n"
    # values
    for i in range(0, len(categories_)):
        ao = categories_[i]
        orgData += "\\armyorganizationcategoryandlimit{" + ao['name'] + "}{\\armylist"
        if ao['minimum'] and 100 > ao['value'] > 0:
            orgData += "min{" + str(ao['value']) + "}}"
        elif not ao['minimum'] and 100 > ao['value'] > 0:
            orgData += "max{" + str(ao['value']) + "}}"
        else:
            orgData += "nolimit{}}"

        if i < len(categories_) - 1:
            orgData += "&\n"
        else:
            orgData += "\\tabularnewline\n"
    template = template.replace(ARMY_ORG_DATA_BALISE, orgData)
    return template


def gen_restrictions(u: {}):
    restrictions = ""
    if not "restrictions" in u:
        return restrictions
    listRestriction = list(u['restrictions'].keys())
    for i in range(0, len(listRestriction)):
        if listRestriction[i] == "maxPerArmy":
            if "mount" in u['categories']:
                restrictions += f"maxmountsperarmy={u['restrictions'][listRestriction[i]]},\n"
            else:
                restrictions += f"maxunitsperarmy={u['restrictions'][listRestriction[i]]},\n"
        elif listRestriction[i] == "maxModelsPerArmy":
            restrictions += f"addrestriction=\\zerotoXmodelsperarmy{{{u['restrictions'][listRestriction[i]]}}},\n"
        elif listRestriction[i] == "sharedMaxPerArmy":
            restrictions += f"addrestriction=\\zerotoXunitsperarmy{{{u['restrictions'][listRestriction[i]]}}}\\refsymbol{{}},\n"
        elif listRestriction[i] == "specialNote":
            restrictions += f"categorynote={u['restrictions'][listRestriction[i]]},\n"
        else:
            logger_router.error(f"unknown restriction: {listRestriction[i]}")
    return restrictions


def gen_base_size(base: {}):
    if base['depth'] > 0:
        res = f"{base['width']}\\timess{base['depth']}"
    else:
        res = f"{base['width']}"

    return res


def gen_unit_type(el: str):
    return "\\" + el.lower() + "{}"


def gen_unit_height(el: str):
    return "\\height" + el.lower() + "{}"


def gen_profile(profile: {}):
    res = ""
    res += f"global@Ad={profile['global']['advanceRate']},\n"
    res += f"global@Ma={profile['global']['marchRate']},\n"
    res += f"global@Di={profile['global']['discipline']},\n"
    if 'rules' in profile['global']:
        rules = ""
        for r in profile['global']['rules']:
            rules += f"{r['name']},"
        res += f"globalrules={{{rules}}},\n"

    res += f"defense@HP={profile['defense']['hp']},\n"
    res += f"defense@Df={profile['defense']['defensiveSkill']},\n"
    res += f"defense@Re={profile['defense']['resistance']},\n"
    res += f"defense@Arm={profile['defense']['armour']},\n"
    if 'rules' in profile['defense']:
        rules = ""
        for r in profile['defense']['rules']:
            if not r['equipment']:
                rules += f"{r['name']},"
        res += f"defenserules={{{rules}}},\n"
        rules = ""
        for r in profile['defense']['rules']:
            if r['equipment']:
                rules += f"{r['name']},"
        res += f"defensearmour={{{rules}}},\n"
    for i in range(0, len(profile['offenses'])):
        off = profile['offenses'][i]
        suffix = "" if i == 0 else ['B', 'C', 'D', 'E', 'F', 'G'][i - 1]
        res += f"offensename{suffix}={off['name']},\n"
        res += f"offense{suffix}@At={off['attacks']},\n"
        res += f"offense{suffix}@Of={off['offensiveSkill']},\n"
        res += f"offense{suffix}@St={off['strength']},\n"
        res += f"offense{suffix}@AP={off['ap']},\n"
        res += f"offense{suffix}@Ag={off['agility']},\n"
        if 'rules' in off:
            rules = ""
            for r in off['rules']:
                if not r['equipment']:
                    rules += f"{r['name']},"
            res += f"offenserules{suffix}={{{rules}}},\n"
            rules = ""
            for r in off['rules']:
                if r['equipment']:
                    rules += f"{r['name']},"
            res += f"offenseweapons{suffix}={{{rules}}},\n"
    return res


def gen_options(options: []):
    if len(options) == 0:
        return ""
    res = "options={%\n"
    optionLines = ""
    for option in options:
        if 'isMount' in option and option['isMount']:
            continue
        if 'isMagic' in option and option['isMagic']:
            continue
        if 'isCommandGroup' in option and option['isCommandGroup']:
            continue
        if len(option['values']) > 0 and len(option['globalPrice']) == 0:
            optionLines += f"{option['globalName']}{{\\AlCoOrder{{%\n"
            optionLines = add_sub_options(option, optionLines, "", False)
            optionLines += f"}}}},\n"
        else:
            mainLine = f"{option['globalName']}={option['globalPrice']}"
            optionLines += f"{mainLine},\n"
            optionLines = add_sub_options(option, optionLines, mainLine, False)

    if optionLines == "":
        return ""
    return res + optionLines + "},\n"


def add_sub_options(option, optionLines, mainLine, isCommandGroup):
    ordering = f"\\alphaorderstickto{{{mainLine}}}" if len(mainLine) > 0 and isCommandGroup else ""
    for v in option['values']:
        optionLines += f"{ordering}{v['name']}={v['price']},\n"
    return optionLines


def gen_options_mounts(options: []):
    if len(options) == 0:
        return ""
    res = "mounts={%\n"
    optionLines = ""
    for option in options:
        if 'isMount' not in option or not option['isMount']:
            continue
        optionLines += f"{option['globalName']}={option['globalPrice']},\n"
    if optionLines == "":
        return ""
    return res + optionLines + "},\n"


def gen_options_magic(options: []):
    if len(options) == 0:
        return ""
    res = "magic={%\n"
    optionLines = ""
    for option in options:
        if 'isMagic' not in option or not option['isMagic']:
            continue
        mainLine = f"{option['globalName']}={option['globalPrice']}"
        optionLines += f"{mainLine},\n"
        optionLines = add_sub_options(option, optionLines, mainLine, False)
    if optionLines == "":
        return ""
    return res + optionLines + "},\n"


def gen_options_cg(options: []):
    if len(options) == 0:
        return ""
    res = "commandgroup={%\n"
    optionLines = ""
    for option in options:
        if 'isCommandGroup' not in option or not option['isCommandGroup']:
            continue
        mainLine = f"{option['globalName']}={option['globalPrice']}"
        optionLines += f"{mainLine},\n"
        optionLines = add_sub_options(option, optionLines, mainLine, True)
    if optionLines == "":
        return ""
    return res + optionLines + "},\n"


def gen_unit_specific_rules(u, army, isFromOption: bool):
    if "modelRules" not in u or len(u['modelRules']) == 0:
        return ""
    res = "{%\n"
    rules = []
    for r in u['modelRules']:
        ruleName = r['name']
        found = False
        for o in u['options']:
            if ruleName in o['globalName']:
                found = True
                break
            for v in o['values']:
                if ruleName in v['name']:
                    found = True
                    break
        if found == isFromOption:
            rules.append(r)
    if len(rules) == 0:
        return ""
    for r in rules:
        res += f"		\\modelruledef{{{r['name']}}}{{\\ruletype{{{gen_rule_type(r['type'], True)}}}{r['rules']}}}\n"
    return res + "}"


def gen_paths(u):
    if "paths" not in u or len(u['paths']) == 0:
        return ""
    res = "paths={%\n"
    for p in u['paths']:
        res += f"\\{p}{{}}={p},"
    return res + "\n},\n"


def is_scoring(u):
    for r in u['profile']['global']['rules']:
        if 'scoring' == r['name'].replace('{}', '').replace('\\', ''):
            return True
    return False


def gen_additional_categories(u, categories):
    if len(u['categories']) == 1:
        return ""
    if len(u['categories']) > 2:
        logger_router.error("can't deal with more than 2 categories")
        return ""
    mainCategory = None
    otherCategory = None
    for c in categories:
        if c['name'] == u['categories'][0]:
            mainCategory = c
        if c['name'] == u['categories'][1]:
            otherCategory = c
    return f"secondlogo={otherCategory['logo']},\n" \
           f"categorynote=\\twocategoriesnote{{{mainCategory['name']}}}{{{otherCategory['name']}}},\n"


def gen_category_change(u, categories):
    if 'categoryChange' not in u:
        return ""
    return f"optionallogo=core,\ncategorynote={u['categoryChange']['condition']},\n"


def gen_units_internal(category: {}, unitList: [], army: {}):
    limitVal = "\\armylist"
    if category['minimum'] and 100 > category['value'] > 0:
        limitVal += "min{" + str(category['value']) + "}"
    elif not category['minimum'] and 100 > category['value'] > 0:
        limitVal += "max{" + str(category['value']) + "}"
    else:
        limitVal += "nolimit{}"
    titleName = category['name'].replace('\\', '').replace('{}', '')
    res = f"\\armylisttitle{{{titleName}}}{{{category['name']}}}{{{limitVal}}}\n"
    for u in unitList:
        res += f"\\unitentry{{%\nname={u['name']}{{}},\n" \
               f"logo={category['logo']},\n" \
               f"fluff={u['fluff'] if 'fluff' in u else ''},\n" \
               f"{gen_additional_categories(u, army['armyOrganisation']['categories'])}" \
               f"{gen_category_change(u, army['armyOrganisation']['categories'])}" \
               f"cost={u['cost'] if u['cost'] > 0 else ''},\n" \
               f"unitsize={u['unitSize'] if u['unitSize'] > 0 else ''},\n" \
               f"maxunitsize={u['maxunitsize'] if 'maxunitsize' in u and u['maxunitsize'] > 0 else ''},\n" \
               f"costpermodel={u['costpermodel'] if 'costpermodel' in u and u['costpermodel'] > 0 else ''},\n" \
               f"scoring={'yes' if is_scoring(u) else ''},\n" \
               f"{gen_restrictions(u)}" \
               f"type={gen_unit_type(u['type'])},\n" \
               f"size={gen_unit_height(u['height'])},\n" \
               f"basesize={gen_base_size(u['baseSize'])},\n" \
               f"{gen_profile(u['profile'])},\n" \
               f"{gen_options(u['options'])}" \
               f"{gen_options_mounts(u['options'])}" \
               f"{gen_options_magic(u['options'])}" \
               f"{gen_options_cg(u['options'])}" \
               f"{gen_paths(u)}" \
               f"modelrulesdef={gen_unit_specific_rules(u, army, False)},\n" \
               f"optionalmodelrulesdef={gen_unit_specific_rules(u, army, True)},\n" \
               f"}} % END UNIT ENTRY\n"
    return res + "\\clearpage\n"


def gen_army_list(army: {}, template: str):
    categories_ = army['armyOrganisation']['categories']
    listData = ""
    for c in categories_:
        logger_router.info(f"category: {c['name']}")
        unitList = [u for u in army['armyList']['units'] if c['name'] == u['categories'][0]]
        logger_router.info(f"units: {unitList}")
        if len(unitList) > 0:
            listData += gen_units_internal(c, unitList, army)
        if "character" in c['name']:
            # we add the mounts
            unitList = [u for u in army['armyList']['units'] if 'mount' == u['categories'][0]]
            if len(unitList) > 0:
                listData += gen_units_internal(
                    {"name": "\\charactermounts", "logo": "character", "value": 0, "minimum": False}, unitList, army)
    template = template.replace(ARMY_LIST_BALISE, listData)
    return template


def gen_shooting_weapons(army):
    res = "\\centeredsubtitle{\\shootingweapons}\n\\startartillerytable\n"
    ruleList = []
    # we search global model rules first
    for r in army['modelRules']['rules']:
        if 'shootingweapon' in r['type'] or 'artilleryweapon' in r['type']:
            ruleList.append(r)
    # then we search individual model rules
    for u in army['armyList']['units']:
        if 'modelRules' not in u:
            continue
        for r in u['modelRules']:
            if 'shootingweapon' in r['type'] or 'artilleryweapon' in r['type']:
                ruleList.append(r)
    if len(ruleList) == 0:
        return ""
    for r in ruleList:
        definitionFlag = 'definition' if 'definition' in r else 'rules'
        definition = army['loc']['en'][r[definitionFlag].replace('{}', '')]
        logger_router.info("def: " + definition)
        rangeFlag = '\\range{'
        stFlag1 = '\\Strength{}'
        stFlag2 = '\\St{}'
        apFlag1 = '\\ArmourPenetration{}'
        apFlag2 = '\\AP{}'
        shotsFlag = '\\shots{'
        rangeWeapon = "-"
        artillery = "-"
        st = "-"
        ap = "-"
        shots = "-"
        attackattributes = "-"
        remainingRules = ""

        if rangeFlag in definition:
            rangeWeapon = definition[definition.index(rangeFlag) + len(rangeFlag):]
            rangeWeapon = rangeWeapon[:rangeWeapon.index('}')]
        if shotsFlag in definition:
            shots = definition[definition.index(shotsFlag) + len(shotsFlag):]
            shots = shots[:shots.index('}')]

        patternAttribute = r" *([a-zA-Z0-9]+?).*"
        try:
            if stFlag1 in definition:
                st = definition[definition.index(stFlag1) + len(stFlag1):]
                p = re.compile(patternAttribute)
                st = p.match(st).group(1)
        except:
            pass
        try:
            if stFlag2 in definition:
                st = definition[definition.index(stFlag2) + len(stFlag2):]
                p = re.compile(patternAttribute)
                st = p.match(st).group(1)
        except:
            pass
        try:
            if apFlag1 in definition:
                ap = definition[definition.index(apFlag1) + len(apFlag1):]
                p = re.compile(patternAttribute)
                ap = p.match(ap).group(1)
        except:
            pass
        try:
            if apFlag2 in definition:
                ap = definition[definition.index(apFlag2) + len(apFlag2):]
                p = re.compile(patternAttribute)
                ap = p.match(ap).group(1)
        except:
            pass
        rulesFound = []
        initSearch = definition
        pattern = r"(\\.*?)\{"
        rulePattern = re.compile(pattern)
        potentialRules = []
        for match in rulePattern.finditer(initSearch):
            flag = match.group(1)

            found = False
            for forbidden in [rangeFlag, stFlag1, stFlag2, apFlag1, apFlag2, shotsFlag]:
                if flag in forbidden:
                    found = True
                    break
            if found:
                if len(potentialRules) > 0:
                    # we cut the previous rule to here
                    potentialRules.append(('', match.start(), 0))

                continue
            if not flag in army['loc']['en']:
                continue
            potentialRules.append((flag, match.start(), match.end()))

        for i in range(0, len(potentialRules)):
            data = ""
            match = potentialRules[i]
            if match[0] == '':
                continue
            if i < len(potentialRules) - 1:
                data = initSearch[match[2] - 1:potentialRules[i + 1][1]]
            else:
                data = initSearch[match[2] - 1:]

            countBrackets = 0
            bracketsToRemove = []
            for i in range(0, len(data)):
                if data[i] == '{':
                    countBrackets += 1
                if data[i] == '}':
                    countBrackets -= 1
                    if countBrackets < 0:
                        bracketsToRemove.append(i)
                        countBrackets += 1
            removedNb = 0
            for i in bracketsToRemove:
                data = data[:i - removedNb] + data[i - removedNb + 1:]
                removedNb += 1
            data = data.replace('.', '').replace(',', '')
            rulesFound.append((match[0], data))

        if len(rulesFound) > 0:
            if 'artilleryweapon' in r['type']:
                artillery = ""
                index = -1
                for rule in rulesFound:
                    index += 1
                    if rule[0] in ['\\catapult', '\\cannon', '\\flamethrower', '\\volleygun']:
                        artillery = rule[0] + rule[1]
                        break
                if index >= 0:
                    del rulesFound[index]
            attackattributes = ""
            for rule in rulesFound:
                attackattributes += rule[0] + rule[1] + ","

        res += f"{r['name'].replace('{}', '')}{{}} & {artillery} & \\distance{{{rangeWeapon}}} & {st} & {ap} & {shots} & \\alphaorderlistpar{{{attackattributes}}}{remainingRules}  \\tabularnewline\n"
    return res + "\\closeartillerytable\n"


def gen_aim_table(army):
    res = "\\centeredsubtitle{\\aimtable}\n\\startaimtable\n"
    weaponsList = []

    # then we search individual profile
    for u in army['armyList']['units']:
        for o in u['profile']['offenses']:
            for w in o['rules']:
                if w['equipment'] and '(' in w['name']:
                    weaponsList.append((u['name'], w['name']))
        # and in options
        for o in u['options']:
            search = []
            search.append(o['globalName'])
            for v in o['values']:
                search.append(v['name'])
            for w in search:
                if re.match(r".*\( *[0-9]\+ *\).*", w):
                    weaponsList.append((u['name'], w))
    if len(weaponsList) == 0:
        return ""
    logger_router.info(weaponsList)
    for w in weaponsList:
        logger_router.info(w)
        match = re.match(r".*(\\[a-zA-Z]+?)\{\}+? *\( *([0-9]\+) *\).*", w[1])
        name = match.group(1)
        aim = match.group(2)

        res += f"{name.replace('{}', '')}{{}} & {aim}  & {w[0].replace('{}', '')}{{}} \\tabularnewline\n"
    return res + "\\closeaimtable\n"


def gen_qrs(army, template):
    template = template.replace(QRS_SHOOTING_WEAPONS_BALISE, gen_shooting_weapons(army))
    template = template.replace(QRS_AIM_TABLE_BALISE, gen_aim_table(army))
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
