CREATE TABLE sensordata (
    date_time DATETIME,
    hum_indoor FLOAT,
    temp_indoor FLOAT,
    hum_outdoor FLOAT,
    temp_outdoor FLOAT,
    water_level FLOAT,
    soil_moisture FLOAT,
    soil_moisture_raw INT
);

CREATE TABLE arduinolog (
    date_time DATETIME,
    log_message text
);