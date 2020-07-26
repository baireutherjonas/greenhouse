import mariadb
from datetime import datetime
import os

def storeData(msgJson):
    __insert(msgJson['indoor']['hum'],msgJson['indoor']['temp'],msgJson['outdoor']['hum'],msgJson['outdoor']['temp'],msgJson['water']['height'],msgJson['soil']['moisture'],msgJson['soil']['moistureraw'])

def storeLogging(message):
    __insertLogging(message)

def __insert(hum_indoor, temp_indoor, hum_outdoor, temp_outdoor, water_level, soil_moisture, soil_moisture_raw):
    try:
        conn = mariadb.connect(
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            host=os.environ['DB_HOST'],
            port=3306,
            database=os.environ['DB_NAME']
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
    # Get Cursor
    cur = conn.cursor()

    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

    cur.execute(
    "INSERT INTO sensordata VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
    (formatted_date, hum_indoor, temp_indoor, hum_outdoor, temp_outdoor, water_level, soil_moisture, soil_moisture_raw))

    conn.commit()

def __insertLogging(message):
    try:
        conn = mariadb.connect(
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            host=os.environ['DB_HOST'],
            port=3306,
            database=os.environ['DB_NAME']
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
    # Get Cursor
    cur = conn.cursor()

    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

    cur.execute(
    "INSERT INTO arduinolog VALUES (?, ?)", 
    (formatted_date, message))

    conn.commit()


