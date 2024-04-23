from flask import Flask, jsonify
from w1thermsensor import W1ThermSensor, Unit
import time

app = Flask(__name__)

names = {
    '031654c65fff': 'Paduodamas', # 28-031654c65fff
    '0214630b7cff': 'Gryztamas', # 28-0214630b7cff
    '0214633567ff': 'Zidinys' # 28-0214633567ff
}

# Function to read temperature from DS18B20 sensor using w1thermsensor
def read_temperature(sensor):
    try:
        # sensor.set_resolution(10, persist=False)  # Set resolution to 10 bits, not persisting between reboots
        temperature = sensor.get_temperature(Unit.DEGREES_C)
        return round(temperature, 5)  # Precision up to 0.1 degrees
    except Exception as e:
        print(f"Error reading sensor {sensor.id}: {e}")
    return None

# Endpoint to get temperatures from all sensors
@app.route('/temperature', methods=['GET'])
def get_temperatures():
    start = time.time()
    temperatures = {}
    for sensor in W1ThermSensor.get_available_sensors():
        temperature = read_temperature(sensor)
        if temperature is not None:
            sensor_id = sensor.id
            name = names.get(sensor_id, "Unknown Sensor")
            temperatures[name] = {
                "sensor_name": name,
                "sensor_id": sensor_id,
                "temperature": temperature
            }
    t = (int)((time.time() - start) * 1000)
    print(f"Elapsed time: {t} ms.")

    gryztamas_tmp = temperatures.get("Gryztamas", {}).get("temperature", "Nera duomenu")
    paduodamas_tmp = temperatures.get("Paduodamas", {}).get("temperature", "Nera duomenu")
    zidinys_tmp = temperatures.get("Zidinys", {}).get("temperature", "Nera duomenu")
    return f"""
        <html>
            <head>
                <title>Temperatura</title>
                <meta http-equiv="refresh" content="1">
            </head>
            <body>
                <div style="font-size: 50px;">
                    Temperaturos
                </div>
                <div style="font-size: 50px;">
                    <div>Zidinys: {zidinys_tmp} C°</div>
                    <div>Paduodamas i grindis: {paduodamas_tmp} C°</div>
                    <div>Gryztamas is grindu: {gryztamas_tmp} C°</div>
                </div>

            </body>
        </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run the Flask app on all available network interfaces
