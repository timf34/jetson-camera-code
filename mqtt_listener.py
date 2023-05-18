import json
import os
import sys
import threading
from time import time, sleep

from typing import Union, Dict

from aws_iot.iot_config import *
from aws_iot.IOTClient import IOTClient
from aws_iot.IOTContext import IOTContext, IOTCredentials
from camera_utils.logger import Logger
from camera_utils.utility_funcs import get_log_file_path
sys.path.append("../TriangulationAndErrorHandling")
from triangulation_logic import create_tracker_instance, MultiCameraTracker, Detections, ThreeDPoints

received_all_event = threading.Event()

# Start a timer at 0 seconds
start_time = time()


class MQTTListener:
    def __init__(
            self,
            iot_manager: IOTClient,
            logger: Logger,
            tracker: MultiCameraTracker = None,
    ):
        self.iot_manager = iot_manager
        self.logger = logger
        self.received_message: str = ""
        self.received_count: int = 0
        self.elapsed_time = 0
        self.tracker: MultiCameraTracker = tracker
        
        # TODO: add a comment explaining or get rid of this. 
        self.detections: Dict = {
            "0": {"message": "", "timestamp": 0},
            "1": {"message": "", "timestamp": 0},
            "currentTime": 0.,  # For debugging
        }

    def on_message_received(self, topic, payload, dup, qos, retain, **kwargs) -> None:
        print(f"Received message from topic '{topic}' at {time()}: {payload}")


        self.received_count += 1
        self.received_message = payload
        self.logger.log(f"Received Message : {self.received_message}")

        end_time = time()
        self.elapsed_time = end_time - start_time
        print(f"Received {self.received_count} messages in {self.elapsed_time} seconds")

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

    def prepare_to_receive(self) -> None:
        try:
            self.iot_manager.connect()
            self.iot_manager.subscribe(topic=CAMERA_TOPIC, handler=self.on_message_received)
            if not received_all_event.is_set():
                self.logger.log("Waiting to receive message.")
        except Exception as e:
            self.logger.log(f"Error preparing to receive: {e}")
            raise

    def decode_received_message(self) -> None:
        try:
            # If received message is of type bytes, decode it.
            if isinstance(self.received_message, bytes):
                if self.received_message != '':
                    self.received_message = self.received_message.decode("utf-8")
        except Exception as e:
            self.logger.log(f"Error decoding message: {e}")
            raise

    def process_received_message(self) -> None:
        try:
            received_message_json = json.loads(self.received_message)
            received_message_json["timestamp"] = self.elapsed_time
            self.update_detections_dict(received_message_json)

            # TODO: Here I would convert the received_message to a Detections object and pass it to the tracker.

            self.logger.log(f"Publishing message: {self.detections}")
            self.iot_manager.publish(
                topic=self.iot_manager.publish_topic,
                payload=json.dumps(self.detections)
            )
        except Exception as e:
            self.logger.log(f"Error processing message: {e}")
            raise

    def wait_for_new_message(self) -> None:
        temp_received_count = self.received_count
        while temp_received_count == self.received_count:
            sleep(0.01)

    def cleanup(self) -> None:
        try:
            received_all_event.wait()
            self.iot_manager.disconnect()
        except Exception as e:
            self.logger.log(f"Error during cleanup: {e}")
            raise

    def main_loop(self) -> None:
        while True:
            try:
                self.decode_received_message()
                if len(self.received_message) == 0:
                    print("received_message is empty. Continuing...")
                    continue
                self.process_received_message()
                self.wait_for_new_message()
            except KeyboardInterrupt:
                print("KeyboardInterrupt received. Exiting...")
                break
            except Exception as e:
                self.logger.log(f"Error in main loop: {e}")
                break

    def run(self) -> None:
        try:
            self.prepare_to_receive()
            self.main_loop()
        except Exception as e:
            self.logger.log(f"Error during run: {e}")
        finally:
            self.cleanup()


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
    iot_client = IOTClient(iot_context, iot_credentials, subscribe_topic=CAMERA_TOPIC, publish_topic=DEVICE_TOPIC)
    log_file_path = get_log_file_path(jetson_name="mqtt_listener")
    mqtt_listener = MQTTListener(iot_manager=iot_client, logger=Logger(log_file_path=log_file_path, buffer_size=10))

    mqtt_listener.run()
