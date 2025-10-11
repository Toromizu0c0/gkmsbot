import json

def get_json():
    filepath = "./niacalc_config.json"
    with open(filepath, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config