import fileinput
import requests
import json

url = "http://192.168.1.83:3000/visit"

headers = { 'Content-Type' : 'application/json' }

for line in fileinput.input():
    response = requests.get(url, data=json.JSONEncoder().encode({"rut": line.rstrip() }), headers=headers)
