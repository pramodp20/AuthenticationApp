import json
import sys
import os

data = None

def get_json():
    global data
    # Determine the path to the key.json file
    if hasattr(sys, '_MEIPASS'):
        file_path = os.path.join(sys._MEIPASS, 'key.json')
    else:
        file_path = 'key.json'

    with open(file_path, 'r') as file:
        data = json.load(file)

    return data

def get_accounts():
    return get_json()
