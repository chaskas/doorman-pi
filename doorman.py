import fileinput
import requests
import json

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

GPIO.setup(15, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)

#url = "http://xsknet.dyndns.org:82/visit"
url = "http://192.168.1.66:3000/visit"

headers = { 'Content-Type' : 'application/json' }

for line in fileinput.input():
    response = requests.get(url, data=json.JSONEncoder().encode({"rut": line.rstrip() }), headers=headers)
    GPIO.output(15, GPIO.HIGH)
    GPIO.output(16, GPIO.HIGH)
    sleep(5) 
    GPIO.output(15, GPIO.LOW)
    GPIO.output(16, GPIO.LOW)
