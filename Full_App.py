#!/usr/bin/env python

import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="attendanceadmin",
    passwd="tariq",
    database="attendancesystem",
)

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
cursor = db.cursor()
reader = SimpleMFRC522()

try:
  while True:

    id, text = reader.read()

    cursor.execute("Select id, name FROM users WHERE rfid_uid="+str(id))
    result = cursor.fetchone()
    if cursor.rowcount >= 1:
      print("User scanned with id: "+str(id))
      cursor.execute("INSERT INTO attendance (user_id) VALUES (%s)", (result[0],) )
      db.commit()
      GPIO.output(18, GPIO.HIGH)
      time.sleep(3)
      GPIO.output(18, GPIO.LOW)
    else:
        print("Unkown user: "+str(id))
        time.sleep(1)
except KeyboardInterrupt:
    print("stopping")
    GPIO.cleanup()
finally:
  GPIO.cleanup()
