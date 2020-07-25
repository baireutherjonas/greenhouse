from flask import Flask, render_template
import mariadb 
import pandas as pd

# Create the application instance
app = Flask(__name__)

# Create a URL route in our application for "/"
@app.route('/')
def stat():
    conn = mariadb.connect(
        user="green",
        password="house",
        host="db",
        database="greenhouse")
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

    c.execute("SELECT * from arduinolog ORDER BY date_time DESC LIMIT 20")
    loggerresult = c.fetchall()

    c.close()

    df = pd.read_sql_query("SELECT * from sensordata ORDER BY date_time DESC  LIMIT 400", conn)

    # verify that result of SQL query is stored in the dataframe
    print(df.to_json())

    conn.close()

    time = df['date_time'].values.tolist() # x axis
    data1 = df['temp_indoor'].values.tolist()
    data2 = df['temp_outdoor'].values.tolist()
    soil = df['soil_moisture'].values.tolist()

    print(type(time[1]))

    print(data1)

    return render_template('weather.html', date=date, air_temp=air_temp, air_hum=air_hum,air_temp_outdoor=air_temp_outdoor, air_hum_outdoor=air_hum_outdoor, soil_temp=soil_temp,  time=time, data1=data1, data2=data2, soil=soil, loggerresult=loggerresult)

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)
