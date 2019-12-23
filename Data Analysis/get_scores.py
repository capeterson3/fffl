import json

with open('week_2scoreboard.json') as json_file:
    data = json.load(json_file)
    print(data)
