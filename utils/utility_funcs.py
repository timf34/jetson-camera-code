import json
import os
import socket
import time

from typing import Dict, List


def get_ip_address() -> str:
    """Get the IP address of the device"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def save_to_json_file(data: Dict[str, List], dir: str = "../logs/jetson3") -> None:
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