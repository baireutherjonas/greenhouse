import mariadb
from datetime import datetime

def storeData(config, msgJson):
    __insert(config, msgJson['indoor']['hum'],msgJson['indoor']['temp'],msgJson['outdoor']['hum'],msgJson['outdoor']['temp'],msgJson['water']['height'],msgJson['soil']['moisture'],msgJson['soil']['moistureraw'])

def storeLogging(config, message):
    __insertLogging(config, message)

def __insert(config, hum_indoor, temp_indoor, hum_outdoor, temp_outdoor, water_level, soil_moisture, soil_moisture_raw):
    try:
        conn = mariadb.connect(
            user=config.get('Database','USER'),
            password=config.get('Database','PASSWORD'),
            host=config.get('Database','HOST'),
            port=3306,
            database=config.get('Database','DB_NAME')

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

def __insertLogging(config, message):
    try:
        conn = mariadb.connect(
            user=config.get('Database','USER'),
            password=config.get('Database','PASSWORD'),
            host=config.get('Database','HOST'),
            port=3306,
            database=config.get('Database','DB_NAME')

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


