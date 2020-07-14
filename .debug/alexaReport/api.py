import requests
import json


r = requests.get('https://coronavirus-tracker-api.herokuapp.com/v2/locations').json()
print(r["latest"]["confirmed"])
print(r["latest"]["deaths"])
print(r["latest"]["recovered"])

# print(r["locations"])