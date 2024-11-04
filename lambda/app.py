import json
import os

import boto3


def cleanup(schedule_name):
    # Initialize the EventBridge Scheduler client
    scheduler = boto3.client('scheduler')

    try:
        # Delete the schedule directly
        scheduler.delete_schedule(Name=schedule_name)
        print(f"Successfully cleaned up the schedule: {schedule_name}")
    except Exception as e:
        print(f"Error cleaning up the schedule: {e}")


def publish_to_mqtt_topic(state):
    topic = os.getenv('MQTT_TOPIC')
    iot_client = boto3.client('iot-data', region_name='us-east-1')
    # Publish the message to the MQTT topic
    response = iot_client.publish(
        topic=topic,
        qos=1,
        payload=json.dumps({'LED': state}),
        retain=True  # Retain message to persist on/off state at ESP32 boot
    )
    print(f"response:\r{response}")


def lambda_handler(event, context):
    print(f'event:\r{event}')

    state = event.get('light_switch')
    print(f"light_switch:\r{state}")

    publish_to_mqtt_topic(state)

    my_schedule_name = event.get('schedule_name')
    print(f"my_schedule_name:\r{my_schedule_name}")

    cleanup(my_schedule_name)
