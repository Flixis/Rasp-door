#!/usr/bin/env python
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="attendanceadmin",
  passwd="Sitecom12",
  database="attendancesystem"
)

cursor = db.cursor()
reader = SimpleMFRC522()
try:
  while True:

    id, text = reader.read()

    cursor.execute("Select id, name FROM users WHERE rfid_uid="+str(id))
    result = cursor.fetchone()
    if cursor.rowcount >= 1:

      cursor.execute("INSERT INTO attendance (user_id) VALUES (%s)", (result[0],) )
      db.commit()
    else:
        time.sleep(2)
finally:
  GPIO.cleanup()