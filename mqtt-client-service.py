import json
import time
import paho.mqtt.client as mqtt
import pymongo
import os
from dotenv import load_dotenv

load_dotenv()
os.environ['TZ'] = 'Asia/Jakarta'

try:
    mongo = pymongo.MongoClient(os.getenv('MONGO_URI'))
    db = mongo['chart']
    collection = db['sensor']
except Exception as e:
    print(f"Error: {str(e)}")


def on_connect(client, userdata, flags, rc, properties):
    print(f"Connected with result code {str(rc)}")
    client.subscribe('iot/#')


def on_message(client, userdata, msg):
    topic = msg.topic
    print(f"data received from topic: {topic}")
    if topic == 'iot/sensor':
        data = json.loads(str(msg.payload.decode("utf-8")))
        data['timestamp'] = int(time.time())
        if collection.count_documents({}) >= 20:
            collection.delete_one({})
        collection.insert_one(data)
        print(data)


if __name__ == '__main__':
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message

    client.username_pw_set(os.getenv('MQTT_USERNAME'), os.getenv('MQTT_PASSWORD'))
    client.connect(host=os.getenv('MQTT_HOST'), port=1883, keepalive=60)
    client.loop_start()

    run = True
    while run:
        time.sleep(1)

    client.loop_stop()
    client.disconnect()
