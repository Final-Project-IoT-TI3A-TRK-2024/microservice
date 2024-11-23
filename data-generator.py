import json
import random
import time
import paho.mqtt.client as mqtt


def generate_humidity():
    return random.randint(20, 100)


def generate_temperature():
    return random.randint(10, 40)


def generate_soil_moisture():
    return random.randint(40, 100)


if __name__ == '__main__':
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.username_pw_set('reky', 'reky.iot')
    client.connect(host="mqtt.rekycode.id", port=1883, keepalive=60)

    run = True
    while run:
        humidity = generate_humidity()
        temperature = generate_temperature()
        soil_moisture = generate_soil_moisture()

        data = {
            'timestamp': int(time.time()),
            'humidity': humidity,
            'temperature': temperature,
            'soil_moisture': soil_moisture
        }

        client.publish('iot/sensor', json.dumps(data))
        time.sleep(2)