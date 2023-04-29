import argparse
import json
import os
import threading
from time import time, sleep

# from config import *
CAMERA_TOPIC: str = "cameras/bohs"
from IOTClient import IOTClient
from IOTContext import IOTContext, IOTCredentials


received_count: int = 0
count: int = 0
received_all_event = threading.Event()

# Start a timer at 0 seconds
start_time = time()


def initialize_args():
    parser = argparse.ArgumentParser(description="AWS IoT Core MQTT Client")
    parser.add_argument("-n", "--camera_id", action="store", default="0", dest="camera_id",
                        help="The camera ID (required)")
    parser.add_argument("-c", "--cert_path", action="store",
                        default="./certificates/tims/camera_send_messages/3da7dc68bfa5d09b723ebb9068a96d54550c1555969088ec7398103e772196d2-certificate.pem.crt",
                        dest="cert_path", help="Cert ending in .pem.crt")
    parser.add_argument("-k", "--priv_key_path", action="store",
                        default="./certificates/tims/camera_send_messages/3da7dc68bfa5d09b723ebb9068a96d54550c1555969088ec7398103e772196d2-private.pem.key",
                        dest="priv_key_path", help="Private key ending in .pem.key")
    parser.add_argument("-r", "--root_ca_path", action="store",
                        default="./certificates/tims/camera_send_messages/root.pem",
                        dest="root_ca_path", help="Root CA ending in .pem (usually: AmazonRootCA1.pem")
    parser.add_argument("-u", "--client_id", action="store", default="user5", dest="client_id", help="Username")
    args = parser.parse_args()
    return args


def initialize_iot_manager(args = initialize_args()):

    cwd = os.getcwd()

    iot_context = IOTContext()

    iot_credentials = IOTCredentials(
        cert_path=os.path.join(cwd, args.cert_path),
        client_id=args.client_id,
        endpoint="a13d7wu4wem7v1-ats.iot.eu-west-1.amazonaws.com",
        region="eu-west-1",
        priv_key_path=os.path.join(cwd, args.priv_key_path),
        ca_path=os.path.join(cwd, args.root_ca_path),
    )

    iot_manager = IOTClient(iot_context, iot_credentials, publish_topic=CAMERA_TOPIC)

    return iot_manager


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AWS IoT Core MQTT Client")
    parser.add_argument("-n", "--camera_id", action="store", default="0", dest="camera_id", help="The camera ID (required)")
    parser.add_argument("-c", "--cert_path", action="store",
                        default="./certificates/tims/camera_send_messages/3da7dc68bfa5d09b723ebb9068a96d54550c1555969088ec7398103e772196d2-certificate.pem.crt",
                        dest="cert_path", help="Cert ending in .pem.crt")
    parser.add_argument("-k", "--priv_key_path", action="store",
                        default="./certificates/tims/camera_send_messages/3da7dc68bfa5d09b723ebb9068a96d54550c1555969088ec7398103e772196d2-private.pem.key",
                        dest="priv_key_path", help="Private key ending in .pem.key")
    parser.add_argument("-r", "--root_ca_path", action="store",
                        default="./certificates/tims/camera_send_messages/root.pem",
                        dest="root_ca_path", help="Root CA ending in .pem (usually: AmazonRootCA1.pem")
    parser.add_argument("-u", "--client_id", action="store", default="user5", dest="client_id", help="Username")
    args = parser.parse_args()

    cwd = os.getcwd()

    iot_context = IOTContext()

    iot_credentials = IOTCredentials(
        cert_path=os.path.join(cwd, args.cert_path),
        client_id=args.client_id,
        endpoint="a13d7wu4wem7v1-ats.iot.eu-west-1.amazonaws.com",
        region="eu-west-1",
        priv_key_path=os.path.join(cwd, args.priv_key_path),
        ca_path=os.path.join(cwd, args.root_ca_path),
    )

    iot_manager = IOTClient(iot_context, iot_credentials, publish_topic=CAMERA_TOPIC)
    connect_future = iot_manager.connect()
    connect_future.result()  # Note: .result() needs to be called to ensure that the connection went through - it blocks to wait for the result!

    while True:
        message = json.dumps({
        "camera": args.camera_id,
        "message": f"Test Message {str(count + 1)}",
        })

        print(f"Sending message at {time()}")
        sleep(1)
        iot_manager.publish(payload=message)
        count += 1


    disconnect_future = iot_manager.disconnect()
    disconnect_future.result()
