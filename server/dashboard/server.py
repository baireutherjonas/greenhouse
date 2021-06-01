from flask import Flask, render_template
import mariadb 
import pandas as pd
import datetime
import os

# Create the application instance
app = Flask(__name__)

# Create a URL route in our application for "/"
@app.route('/')
def stat():
    conn = mariadb.connect(
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'])
    c = conn.cursor() 
    
    c.execute("SELECT * from sensordata ORDER BY date_time DESC LIMIT 1")
    records = c.fetchall()

    for row in records:
        date = row[0]
        air_temp=row[2]
        air_hum=row[1]
        air_temp_outdoor=row[4]
        air_hum_outdoor=row[3]
        soil_temp=row[6]

    c.execute("SELECT * from arduinolog ORDER BY date_time DESC")
    loggerresult = c.fetchall()

    c.close()

    df = pd.read_sql_query("SELECT * from sensordata ORDER BY date_time DESC  LIMIT 400", conn)

    conn.close()

    time = []
    f = '%Y-%m-%dT%H:%M:%S'
    for timestamp in df['date_time'].values:
        print(str(timestamp).split(".")[0].replace("T"," "))
        time.append(str(timestamp).split(".")[0].replace("T"," "))

    temp_indoor = df['temp_indoor'].values.tolist()
    temp_outdoor = df['temp_outdoor'].values.tolist()
    soil_moisture = df['soil_moisture'].values.tolist()

    return render_template('weather.html', date=date, air_temp=air_temp, air_hum=air_hum,air_temp_outdoor=air_temp_outdoor, air_hum_outdoor=air_hum_outdoor, soil_temp=soil_temp,  time=time, data1=temp_indoor, data2=temp_outdoor, soil=soil_moisture, loggerresult=loggerresult)

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
