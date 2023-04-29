import json
import os
import threading
from time import time, sleep

from typing import Union, Dict

from aws_iot.iot_config import *
from aws_iot.IOTClient import IOTClient
from aws_iot.IOTContext import IOTContext, IOTCredentials
from utils.logger import Logger
from utils.utility_funcs import get_log_file_path

NUM_MESSAGES = 10

received_count = 0
elapsed_time = 0
received_all_event = threading.Event()

# Start a timer at 0 seconds
start_time = time()


class MQTTListener:
    def __init__(self, iot_manager: IOTClient, logger: Logger):
        self.iot_manager = iot_manager
        self.logger = logger
        self.received_message: str = ""
        self.detections: Dict = {
            "0": {"message": "", "timestamp": 0},
            "1": {"message": "", "timestamp": 0},
            "currentTime": 0.,  # For debugging
        }

    def on_message_received(self, topic, payload, dup, qos, retain, **kwargs) -> None:
        print(f"Received message from topic '{topic}' at {time()}: {payload}")

        global received_count
        global elapsed_time

        received_count += 1
        self.received_message = payload
        self.logger.log(f"Received Message : {self.received_message}")

        end_time = time()
        elapsed_time = end_time - start_time
        print(f"Received {received_count} messages in {elapsed_time} seconds")

        if received_count == NUM_MESSAGES:
            received_all_event.set()

    def update_detections_dict(self, detection: Dict[str, Dict[str, Union[str, float]]]) -> None:

        camera_id = detection["camera"]

        # Update the detection
        self.detections[camera_id]["message"] = detection["message"]
        self.detections[camera_id]["timestamp"] = detection["timestamp"]

        current_elapsed_time = time() - start_time

        self.detections["currentTime"] = current_elapsed_time

        for key in ["0", "1"]:
            if abs(self.detections[key]["timestamp"] - current_elapsed_time) > 0.5:
                self.detections[key]["message"] = ""
                # print(f"Stale detection from camera {key} at {current_elapsed_time}")

    def run(self) -> None:
        # Connect iot_manager
        self.iot_manager.connect()
        # Subscribe to the topic
        self.iot_manager.subscribe(topic=CAMERA_TOPIC, handler=self.on_message_received)

        if not received_all_event.is_set():
            print("Waiting to receive message.")

        while True:
            # If received message is of type bytes, decode it.
            if isinstance(self.received_message, bytes):
                if self.received_message != '':  # Check if empty... the first one probs will be. Note: '' works, "" doesn't.
                    self.received_message = self.received_message.decode("utf-8")
            elif len(self.received_message) == 0:
                print("received_message is empty. Continuing...")
                continue

            received_message_json = json.loads(self.received_message)
            received_message_json["timestamp"] = elapsed_time

            self.update_detections_dict(received_message_json)

            self.logger.log(f"Publishing message: {self.detections}")
            iot_manager.publish(
                topic=iot_manager.publish_topic,
                payload=json.dumps(self.detections)
            )  # Note: detections will be the triangulated coords
            temp_received_count = received_count

            # Wait until a new message is received.
            while temp_received_count == received_count:
                sleep(0.01)

        received_all_event.wait()  # https://docs.python.org/3/library/threading.html#threading.Event.wait used with .set()

        iot_manager.disconnect()


if __name__ == "__main__":
    cwd = os.getcwd()

    iot_context = IOTContext()
    iot_credentials = IOTCredentials(
        cert_path=os.path.join(cwd,
                               "aws_iot/certificates/tims/merger_receive_messages/6c470fd95cb2cd31aa739b052d6e6219d4d35ef11cb1e39d6d852761e84e58f8-certificate.pem.crt"),
        client_id="mergerReceiveMessages",
        endpoint="a13d7wu4wem7v1-ats.iot.eu-west-1.amazonaws.com",
        region="eu-west-1",
        priv_key_path=os.path.join(cwd,
                                   "aws_iot/certificates/tims/merger_receive_messages/6c470fd95cb2cd31aa739b052d6e6219d4d35ef11cb1e39d6d852761e84e58f8-private.pem.key"),
        ca_path=os.path.join(cwd, "aws_iot/certificates/tims/merger_receive_messages/AmazonRootCA1.pem")
    )
    # IOT Manager receive.
    iot_manager = IOTClient(iot_context, iot_credentials, subscribe_topic=CAMERA_TOPIC, publish_topic=DEVICE_TOPIC)
    log_file_path = get_log_file_path(jetson_name="mqtt_listener")
    mqtt_listener = MQTTListener(iot_manager=iot_manager, logger=Logger(log_file_path=log_file_path, buffer_size=10))

    mqtt_listener.run()
