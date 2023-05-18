import json
import os
import socket
import time

from datetime import datetime
from typing import Dict, List

from aws_iot.IOTContext import IOTContext, IOTCredentials
from aws_iot.IOTClient import IOTClient
from config import BohsConfig


def get_log_file_path(jetson_name: str) -> str:
    """
    Returns the path to the log file

    Args:
        jetson_name (str): The name of the jetson device
    """
    today = datetime.now()
    if os.name == 'nt':
        log_dir = f"{os.getcwd()}/logs/laptop"
    else:
        log_dir = f"{os.getcwd()}/logs/{jetson_name}"
    check_and_create_dir(log_dir)
    return f"{log_dir}/{today.strftime('%d_%m_%Y')}.log"


def get_ip_address() -> str:
    """Get the IP address of the device"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def save_to_json_file(data: Dict[str, List], dir: str = f"{os.getcwd()}/logs/jetson3") -> None:
    """Save the data to a json file"""
    filename = time.strftime("%H%M-%d_%m_%Y") + ".json"
    check_and_create_dir(dir)
    full_path = os.path.join(dir, filename)  # Create the full path to the file

    with open(full_path, "w") as f:
        json.dump(data, f)


def check_and_create_dir(dir_name: str) -> None:
    """Check if the directory exists and create it if it doesn't"""
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        print(f"Created directory: {dir_name}")
    else:
        print(f"Directory {dir_name} already exists")


def get_aws_iot_manager(config: BohsConfig) -> IOTClient:
    """
    This function is responsible for managing the connection to AWS IoT Core.
    It instantiates the IOTClient and IOTCredentials classes.
    Practically, we will be using most of the methods already contained in the IOTClient class.
    """
    iot_context = IOTContext()

    iot_credentials = IOTCredentials(
        cert_path=config.cert_path,
        client_id=config.jetson_number,
        endpoint=config.endpoint,
        priv_key_path=config.private_key_path,
        ca_path=config.root_ca_path
    )
    return IOTClient(iot_context, iot_credentials, publish_topic=config.publish_topic)
