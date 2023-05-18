import json
import os
import threading

from statistics import mean, median, variance
from time import time, sleep
from typing import List

from config import *
from IOTClient import IOTClient
from IOTContext import IOTContext, IOTCredentials

NUM_MESSAGES = 1000
received_all_event = threading.Event()

send_time = 0
merger_receive_time = 0
device_receive_time = 0
received_count = 0


class SingleMessageBenchmark:
    def __init__(self):
        self.merger_receive_latency: List[float] = []
        self.device_receive_latency: List[float] = []
        self.total_latency: List[float] = []

        self.iot_client_send: IOTClient
        self.iot_client_merger: IOTClient
        self.iot_client_device: IOTClient

    def setup(self) -> None:
        # Initializing the IOT clients
        self.iot_client_send: IOTClient = IOTClient(
            context=IOTContext(),
            credentials=IOTCredentials(
                cert_path=r"C:\Users\timf3\OneDrive - Trinity College Dublin\Documents\fov\SebsFovWork\fov\fov-net\certificates\tims\camera_send_messages\3da7dc68bfa5d09b723ebb9068a96d54550c1555969088ec7398103e772196d2-certificate.pem.crt",
                client_id="user5",
                endpoint="a13d7wu4wem7v1-ats.iot.eu-west-1.amazonaws.com",
                region="eu-west-1",
                priv_key_path=r"C:\Users\timf3\OneDrive - Trinity College Dublin\Documents\fov\SebsFovWork\fov\fov-net\certificates\tims\camera_send_messages\3da7dc68bfa5d09b723ebb9068a96d54550c1555969088ec7398103e772196d2-private.pem.key",
                ca_path=r"C:\Users\timf3\OneDrive - Trinity College Dublin\Documents\fov\SebsFovWork\fov\fov-net\certificates\tims\camera_send_messages\root.pem"
            ),
            publish_topic=CAMERA_TOPIC
        )

        self.iot_client_merger: IOTClient = IOTClient(
            context=IOTContext(),
            credentials=IOTCredentials(
                cert_path=r"C:\Users\timf3\OneDrive - Trinity College Dublin\Documents\fov\SebsFovWork\fov\fov-net\certificates\tims\merger_receive_messages\6c470fd95cb2cd31aa739b052d6e6219d4d35ef11cb1e39d6d852761e84e58f8-certificate.pem.crt",
                client_id="mergerReceiveMessages",
                endpoint="a13d7wu4wem7v1-ats.iot.eu-west-1.amazonaws.com",
                region="eu-west-1",
                priv_key_path=r"C:\Users\timf3\OneDrive - Trinity College Dublin\Documents\fov\SebsFovWork\fov\fov-net\certificates\tims\merger_receive_messages\6c470fd95cb2cd31aa739b052d6e6219d4d35ef11cb1e39d6d852761e84e58f8-private.pem.key",
                ca_path=r"C:\Users\timf3\OneDrive - Trinity College Dublin\Documents\fov\SebsFovWork\fov\fov-net\certificates\tims\merger_receive_messages\AmazonRootCA1.pem"
            ),
            subscribe_topic=CAMERA_TOPIC,
            publish_topic=DEVICE_TOPIC
        )

        self.iot_client_device: IOTClient = IOTClient(
            context=IOTContext(),
            credentials=IOTCredentials(
                cert_path=r"C:\Users\timf3\OneDrive - Trinity College Dublin\Documents\fov\SebsFovWork\fov\fov-net\certificates\tims\jetson0\a14899325642fe1cad3a4454d45b988752ec93cdf6a5078a6864bec1f6af838f-certificate.pem.crt",
                client_id="jetson2",
                endpoint="a13d7wu4wem7v1-ats.iot.eu-west-1.amazonaws.com",
                region="eu-west-1",
                priv_key_path=r"C:\Users\timf3\OneDrive - Trinity College Dublin\Documents\fov\SebsFovWork\fov\fov-net\certificates\tims\jetson0\a14899325642fe1cad3a4454d45b988752ec93cdf6a5078a6864bec1f6af838f-private.pem.key",
                ca_path=r"C:\Users\timf3\OneDrive - Trinity College Dublin\Documents\fov\SebsFovWork\fov\fov-net\certificates\tims\jetson0\AmazonRootCA1.pem"
            ),
            subscribe_topic=DEVICE_TOPIC
        )

        # Connecting the clients
        sender_connect_future = self.iot_client_send.connect()
        print(f"Sender connect future result: {sender_connect_future.result()}")
        merger_connect_future = self.iot_client_merger.connect()
        print(f"Merger connect future result: {merger_connect_future.result()}")
        device_connect_future = self.iot_client_device.connect()
        print(f"Device connect future result: {device_connect_future.result()}")

        # Subscribing to topics
        merger_subscribe_future = self.iot_client_merger.subscribe(
            topic=self.iot_client_merger.subscribe_topic,
            handler=self.merger_message_received
        )
        print(f"Merger subscribe future result: {merger_subscribe_future.result()}")

        device_subscribe_future = self.iot_client_device.subscribe(
            topic=self.iot_client_device.subscribe_topic,
            handler=self.device_message_receieved
        )
        print(f"Device subscribe future result: {device_subscribe_future.result()}")

        print("Initialization complete\n\n")

    @staticmethod
    def create_test_message(camera_id: str) -> str:
        test_message = {
            "camera": camera_id,
            "message": "Test message",
            "timestamp": time()
        }
        return json.dumps(test_message)

    def merger_message_received(self, topic, payload, dup, qos, retain, **kwargs) -> None:
        global received_count
        global send_time
        global merger_receive_time

        merger_receive_time = time()
        elapsed_time = merger_receive_time - send_time
        self.merger_receive_latency.append(elapsed_time)

        print(f"Merger received message {received_count} from {topic} in {elapsed_time} seconds; payload: {payload}")

        self.iot_client_merger.publish(topic=self.iot_client_merger.publish_topic, payload=payload)

    def device_message_receieved(self, topic, payload, dup, qos, retain, **kwargs) -> None:
        global received_count
        global send_time
        global device_receive_time

        received_count += 1

        device_receive_time = time()
        merger_to_device_elapsed_time = device_receive_time - merger_receive_time
        total_elapsed_time = device_receive_time - send_time

        self.device_receive_latency.append(merger_to_device_elapsed_time)
        self.total_latency.append(total_elapsed_time)

        print(f"Device received message {received_count} from {topic} in {total_elapsed_time} seconds; "
              f"payload: {payload}; total elapsed time: {total_elapsed_time}\n")

        send_time = time()

        if received_count == NUM_MESSAGES:
            received_all_event.set()

    def script(self) -> None:
        global send_time
        test_message = self.create_test_message(camera_id="0")

        for _ in range(100):
            send_time = time()
            self.iot_client_send.publish(topic=self.iot_client_send.publish_topic, payload=test_message)
            sleep(1)  # Sleeping at the moment just to avoid conflicts with the global timing variables. I should test
                      # this again, sending every 0.25 seconds back to back.

        received_all_event.set()

        print(f"Merger to device latency -> mean: {mean(self.device_receive_latency)}, "
              f"median {median(self.device_receive_latency)},"
              f"variance: {variance(self.device_receive_latency)}")
        print(f"Sender to merger latency -> mean: {mean(self.merger_receive_latency)}, "
              f"median {median(self.merger_receive_latency)}, "
              f"variance: {variance(self.merger_receive_latency)}")
        print(f"Total latency -> mean: {mean(self.total_latency)}, "
              f"median: {median(self.total_latency)}, variance: {variance(self.total_latency)}")


def main():
    benchmark = SingleMessageBenchmark()
    benchmark.setup()
    benchmark.script()


if __name__ == "__main__":
    main()
