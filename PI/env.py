import os
import json

script_path = os.path.abspath(__file__)
env_file_path = os.path.join(os.path.dirname(script_path), "env.json")
with open(env_file_path, 'r') as json_file:
    env = json.load(json_file)