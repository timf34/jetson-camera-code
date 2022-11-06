import json
import os
import socket
import time

from typing import Dict, List

def get_ip_address():
    """
        Returns string - function annotations/ typing does weird stuff to code editor colours...?
    """
    # IP address 
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    # print("The main IP address", s.getsockname()[0])
    return s.getsockname()[0]

def save_to_json_file(data: Dict[str, List]) -> None:
    # Create our filename based off the current time and date
    filename = time.strftime("%H%M-%d_%m_%Y") + ".json"

    # Create the directory if it doesn't exist
    if not os.path.exists("logs/jetson3"):
        os.makedirs("logs/jetson3")

    # Create the full path to the file
    full_path = os.path.join("logs/jetson3", filename)

    # Save the data to the file
    with open(full_path, "w") as f:
        json.dump(data, f)
