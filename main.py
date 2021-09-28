#!/usr/bin/env python

import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="tariq",
  passwd="Sitecom12",
  database="attendancesystem"
)

cursor = db.cursor()
reader = SimpleMFRC522()

try:
  while True:
    id, text = reader.read()

    if cursor.rowcount >= 1:
      overwrite = input("Overwite (Y/N)? ")
      if overwrite[0] == 'Y' or overwrite[0] == 'y':
        time.sleep(1)
        sql_insert = "UPDATE users SET name = %s WHERE rfid_uid=%s"
      else:
        continue;
    else:
      sql_insert = "INSERT INTO users (name, rfid_uid) VALUES (%s, %s)"
    new_name = input("Name: ")

    cursor.execute(sql_insert, (new_name, id))

    db.commit()
    time.sleep(2)
finally:
  GPIO.cleanup()