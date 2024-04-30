from flask import Flask, jsonify
from w1thermsensor import W1ThermSensor, Unit
import time
from sensor_map import names
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)



# Function to read temperature from DS18B20 sensor using w1thermsensor
def read_temperature(sensor):
    try:
        # sensor.set_resolution(10, persist=False)  # Set resolution to 10 bits, not persisting between reboots
        temperature = sensor.get_temperature(Unit.DEGREES_C)
        return round(temperature, 5)  # Precision up to 0.1 degrees
    except Exception as e:
        print(f"Error reading sensor {sensor.id}: {e}")
    return None

# Function to process each sensor and collect temperature
def process_sensor(sensor):
    temperature_data = read_temperature(sensor)
    if temperature_data:
        sensor_id = temperature_data['sensor_id']
        temperature = temperature_data['temperature']
        name = names.get(sensor_id, "Unknown Sensor")
        return {
            "sensor_name": name,
            "sensor_id": sensor_id,
            "temperature": temperature
        }
    return None

# Endpoint to get temperatures from all sensors
@app.route('/temperatura', methods=['GET'])
def get_temperatures():
    start = time.time()
    temperatures = {}
    for sensor in W1ThermSensor.get_available_sensors():
        print(sensor)
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
                <div style="font-size: 60px; text-align: center; margin-top: 100px;">
                    Temperaturos
                </div>
                <div style="font-size: 48px; border: 3px solid red; margin-top: 100px; padding: 10px">
                    <div style="margin-top: 50px;">Zidinys: <span style="font-weight: bold;">{zidinys_tmp} C°</span></div>
                    <div style="margin-top: 50px;">Paduodamas i grindis: <span style="font-weight: bold;">{paduodamas_tmp} C°</span></div>
                    <div style="margin-top: 50px; margin-bottom: 50px;">Gryztamas is grindu: <span style="font-weight: bold;">{gryztamas_tmp} C°</span></div>
                </div>

            </body>
        </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)  # Run the Flask app on all available network interfaces
