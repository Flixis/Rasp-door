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


cursor = db.cursor()
reader = SimpleMFRC522()


terminal_input = input()
while terminal_input != "new_user":
    try:
        while True:

            id, text = reader.read()

            cursor.execute("Select id, name FROM users WHERE rfid_uid=" + str(id))
            result = cursor.fetchone()
            if cursor.rowcount >= 1:
                print("added attendance")
                cursor.execute(
                    "INSERT INTO attendance (user_id) VALUES (%s)", (result[0],)
                )
                db.commit()
            else:
                time.sleep(2)
    finally:
        GPIO.cleanup()

if terminal_input == "new user":
    try:
        while True:
            id, text = reader.read()

            if cursor.rowcount >= 1:
                overwrite = input("Overwite (Y/N)? ")
                if overwrite[0] == "Y" or overwrite[0] == "y":
                    time.sleep(1)
                    sql_insert = "UPDATE users SET name = %s WHERE rfid_uid=%s"
                else:
                    continue
            else:
                sql_insert = "INSERT INTO users (name, rfid_uid) VALUES (%s, %s)"
                new_name = input("Name: ")

                cursor.execute(sql_insert, (new_name, id))

                db.commit()
                time.sleep(2)
    finally:
        GPIO.cleanup()
