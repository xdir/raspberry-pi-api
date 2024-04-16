from flask import Flask, jsonify
import glob
import time

app = Flask(__name__)

# Function to read temperature from DS18B20 sensor
def read_temperature(sensor):
    sensor_path = f"/sys/bus/w1/devices/{sensor}/w1_slave"
    try:
        with open(sensor_path, 'r') as file:
            lines = file.readlines()
            while lines[0].strip()[-3:] != 'YES':
                time.sleep(0.2)
                lines = file.readlines()
            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp_c = float(temp_string) / 1000.0
                return round(temp_c, 1)  # Precision up to 0.1 degrees
    except Exception as e:
        print(f"Error reading sensor {sensor}: {e}")
    return None

# Endpoint to get temperatures from all sensors
@app.route('/temperature', methods=['GET'])
def get_temperatures():
    sensors = glob.glob("/sys/bus/w1/devices/28-*/w1_slave")
    print("Sensors: ")
    print(sensors)
    temperatures = []
    for sensor in sensors:
        sensor_id = sensor.split("/")[5]
        temperature = read_temperature(sensor_id)
        if temperature is not None:
            print(temperature)
            temperatures.append({"sensor_name": "Sensor name", "sensor_id": sensor_id, "temperature": temperature})
    return jsonify({"temperatures": temperatures})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run the Flask app on all available network interfaces
