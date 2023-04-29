import json
import os
import threading
from time import time, sleep

from typing import Union, Dict

from aws_iot.iot_config import *
from IOTClient import IOTClient
from IOTContext import IOTContext, IOTCredentials
# from ..utils.logger import Logger

NUM_MESSAGES = 1000

received_count = 0
elapsed_time = 0
received_message: str = ""
received_all_event = threading.Event()

# Start a timer at 0 seconds
start_time = time()

detections = {
    "0": {"message": "", "timestamp": 0},
    "1": {"message": "", "timestamp": 0},
    "currentTime": 0.,  # For debugging
}


def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    print(f"Received message from topic '{topic}' at {time()}: {payload}")

    global received_count
    global received_message
    global elapsed_time

    received_count += 1
    received_message = payload

    end_time = time()
    elapsed_time = end_time - start_time
    print(f"Received {received_count} messages in {elapsed_time} seconds")

    if received_count == NUM_MESSAGES:
        received_all_event.set()


def update_detections_dict(detection: Dict[str, Dict[str, Union[str, float]]]) -> None:
    global detections

    camera_id = detection["camera"]

    # Update the detection
    detections[camera_id]["message"] = detection["message"]
    detections[camera_id]["timestamp"] = detection["timestamp"]
    current_elapsed_time = time() - start_time
    detections["currentTime"] = current_elapsed_time

    for key in ["0", "1"]:
        if abs(detections[key]["timestamp"] - current_elapsed_time) > 0.5:
            detections[key]["message"] = ""
            detections[key]["timestamp"] = 0
            # TODO: not sure what this was
            # print(f"Stale detection from camera {key} at {current_elapsed_time}")

    # TODO: integrate triangulation code here.


if __name__ == "__main__":
    cwd = os.getcwd()

    iot_context = IOTContext()

    iot_credentials = IOTCredentials(
        cert_path=os.path.join(cwd, "certificates/tims/merger_receive_messages/6c470fd95cb2cd31aa739b052d6e6219d4d35ef11cb1e39d6d852761e84e58f8-certificate.pem.crt"),
        client_id="mergerReceiveMessages",
        endpoint="a13d7wu4wem7v1-ats.iot.eu-west-1.amazonaws.com",
        region="eu-west-1",
        priv_key_path=os.path.join(cwd, "certificates/tims/merger_receive_messages/6c470fd95cb2cd31aa739b052d6e6219d4d35ef11cb1e39d6d852761e84e58f8-private.pem.key"),
        ca_path=os.path.join(cwd, "certificates/tims/merger_receive_messages/AmazonRootCA1.pem")
    )

    # IOT Manager receive.
    iot_manager = IOTClient(iot_context, iot_credentials, subscribe_topic=CAMERA_TOPIC, publish_topic=DEVICE_TOPIC)
    connect_future = iot_manager.connect()
    print("IOT receive manager connected!")

    subscribe_future = iot_manager.subscribe(topic=iot_manager.subscribe_topic, handler=on_message_received)
    subscribe_result = subscribe_future.result()
    print(f"Subscribed with {str(subscribe_result['qos'])}")

    if not received_all_event.is_set():
        print("Waiting to receive message.")

    temp_received_count = 0
    while True:
        # If received message is of type bytes, decode it.
        if isinstance(received_message, bytes):
            if received_message != '':  # Check if empty... the first one probs will be. Note: '' works, "" doesn't.
                received_message = received_message.decode("utf-8")
        elif len(received_message) == 0:
            print("received_message is empty. Continuing...")
            continue

        received_message_json = json.loads(received_message)
        received_message_json["timestamp"] = elapsed_time  # This might be better off with time.time(), or whatever would match the message sent!
        print("received_message_json post whatever: ", received_message_json, "\n")

        # Update the detections dict
        update_detections_dict(received_message_json)

        iot_manager.publish(topic=iot_manager.publish_topic, payload=json.dumps(detections))  # Note: detections will be the triangulated coords
        temp_received_count = received_count

        # Wait until a new message is received.
        while temp_received_count == received_count:
            sleep(0.01)

    print("outside of while loop")
    received_all_event.wait()  # https://docs.python.org/3/library/threading.html#threading.Event.wait used with .set()

    disconnect_future = iot_manager.disconnect()
    disconnect_future.result()
    print("Disconnected!")
