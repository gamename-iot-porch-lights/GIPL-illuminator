import json
import os

import boto3


def lambda_handler(event, context):
    print(f'event:\n{event}')
    topic = os.getenv('MQTT_TOPIC')

    iot_client = boto3.client('iot-data', region_name='us-east-1')

    # Extract the message from the event input
    message = event.get('message')

    print(f"message:\n{message}")

    # Publish the message to the MQTT topic
    response = iot_client.publish(
        topic=topic,
        qos=1,
        payload=json.dumps({'LED': message}),
        retain=True  # Retain message to persist on/off state at ESP32 boot
    )
    print(f"response:\n{response}")
