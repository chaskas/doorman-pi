#!/usr/bin/python3
import fileinput
import requests
import json
import sys

import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

red = 27
green = 17
button = 22

GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.output(red, GPIO.HIGH)
GPIO.output(green, GPIO.HIGH)

url = "http://xsknet.dyndns.org:8080/checkin"
# url = "http://127.0.0.1:3000/checkin"
#url = "http://192.168.1.141:3000/checkin"

headers = { 'Content-Type' : 'application/json' }

try:
  for line in sys.stdin:
    rut = line.rstrip()

    if rut == "exit":
        GPIO.cleanup()
        sys.exit(0)

    data = json.JSONEncoder().encode({"rut": rut })
    response = requests.get(url, data=data, headers=headers)

    if response.status_code >= 200 and response.status_code <= 204:
        # nueva visita
        input_state = GPIO.input(button)
        if response.json()['person']['mtype'] == 0:
            if input_state:
                GPIO.output(green, GPIO.LOW)
                sleep(2)
                GPIO.output(green, GPIO.HIGH)
            else:
                GPIO.output(red, GPIO.LOW)
                sleep(2)
                GPIO.output(red, GPIO.HIGH)
        else:
            if response.json()['remaining_guest'] > 0 and input_state:
                GPIO.output(green, GPIO.LOW)
                sleep(2)
                GPIO.output(green, GPIO.HIGH)
            else:
                GPIO.output(red, GPIO.LOW)
                sleep(2)
                GPIO.output(red, GPIO.HIGH)


    elif response.status_code >= 400:
        GPIO.output(red, GPIO.LOW)
        sleep(2)
        GPIO.output(red, GPIO.HIGH)
    else:
        GPIO.output(red, GPIO.LOW)
        sleep(2)
        GPIO.output(red, GPIO.HIGH)
except KeyboardInterrupt:
  print("Quit")
  GPIO.cleanup()
