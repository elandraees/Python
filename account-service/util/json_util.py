import json


def parse_json(json, key):
    try:
        return json[key]
    except KeyError as e:
        return ""


def parse_str_to_json(s):
    try:
        s = s.replace("\'", "\"")
        return json.loads(s)
    except TypeError as e:
        return s
