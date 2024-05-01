from flask import Flask, jsonify
from w1thermsensor import W1ThermSensor, Sensor
import threading
import time

app = Flask(__name__)

# Shared dictionary to store sensor readings
sensor_data = {}

# Fetch all connected sensor IDs of type DS18B20 at startup
sensor_ids = [sensor.id for sensor in W1ThermSensor.get_available_sensors([Sensor.DS18B20])]
print("Available sensors: ")
print(sensor_ids)

# Function to continuously read temperature
def update_sensor_readings():
    while True:
        for sensor_id in sensor_ids:
            try:
                sensor = W1ThermSensor(sensor_type=Sensor.DS18B20, sensor_id=sensor_id)
                temperature = sensor.get_temperature()
                sensor_data[sensor_id] = temperature
            except Exception as e:
                print(f"Error reading sensor {sensor_id}: {e}")
                sensor_data[sensor_id] = None
        time.sleep(2)  # Adjust based on how frequently you want to update the readings

# Start the background thread
thread = threading.Thread(target=update_sensor_readings)
thread.daemon = True
thread.start()

@app.route('/temperatura/<sensor_id>', methods=['GET'])
def get_temperature(sensor_id):
    # Returns the cached temperature instantly
    temperature = sensor_data.get(sensor_id)
    if temperature is None:
        return jsonify({'error': 'Temperature not available'}), 503
    return jsonify({'temperature': temperature})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
