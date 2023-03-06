import cv2
import datetime
import json
import os
import time

from copy import deepcopy
from datetime import datetime
from torch import Tensor as Tensor
from typing import Tuple

from config import BohsConfig
from utils.fps import FPS
from utils.bohs_net_detector import BohsNetDetector
from utils.utility_funcs import get_ip_address, save_to_json_file, check_and_create_dir

import os
import threading

from config import *
from fov_net.IOTClient import IOTClient
from fov_net.IOTContext import IOTContext, IOTCredentials
from fov_net.camera_send_messages import initialize_iot_manager


received_count: int = 0
count: int = 0
received_all_event = threading.Event()

# Start a timer at 0 seconds
start_time = time.time()


# Constants
DEBUG = False
CURRENT_TIME = datetime.now() # not sure if this is bad practice but it works
WIDTH: int = 1280
HEIGHT: int = 720
FRAME_SIZE = (WIDTH, HEIGHT)
LOG_DIR = f"{os.getcwd()}/logs/laptop"
today = datetime.now()
conf = BohsConfig()


def get_seconds_till_match() -> int:
    """Get the number of seconds till the match starts"""
    current_time = datetime.now()
    time_of_match = current_time.replace(day=current_time.day,
                                       hour=conf.hour,
                                       minute=conf.minute,
                                       second=conf.second,
                                       microsecond=conf.microsecond)
    delta_t = time_of_match-current_time

    print(f"Current time is {current_time}\nTime of the match is {time_of_match}")
    return delta_t.seconds+1


def get_capture() -> cv2.VideoCapture:
    """Check if the OS is using Windows or Linux and return the correct capture object"""
    if os.name == 'nt':
        return cv2.VideoCapture(0)  # Windows
    else:
        return cv2.VideoCapture(
            'nvarguscamerasrc !  video/x-raw(memory:NVMM), width=1920, height=1080, format=NV12, framerate=60/1 ! '
            'nvvidconv ! video/x-raw, width=' + str(WIDTH) + ', height=' + str(HEIGHT) + ', format=BGRx ! '
            'videoconvert ! video/x-raw, format=BGR ! appsink')  # Linux


def create_video_writer(video_name: str) -> cv2.VideoWriter:
    """Create a video writer object"""
    return cv2.VideoWriter(video_name,
                           cv2.VideoWriter_fourcc(*'MJPG'),
                           5, FRAME_SIZE)


def create_datetime_video_name() -> str:
    """Create a video name with the current date and time"""
    now = datetime.now()
    return f"{now.strftime('time_%H_%M_%S_date_%d_%m_%Y_')}.avi"


def initialize_fps_timers() -> Tuple[FPS, FPS, FPS, FPS]:
    """Initialize the FPS timers"""
    avg_fps = FPS()
    reading_fps = FPS()
    writing_fps = FPS()
    bohs_fps = FPS()
    return avg_fps, reading_fps, writing_fps, bohs_fps


def get_timeout(timeout_minute_legnth: int) -> float:
    """Return the time in seconds that the timeout will end"""
    return time.time() + (timeout_minute_legnth * 60)


# TODO: rename this function?
def record_and_detect_match_mode() -> None:
    
    # Initialization
    json_dict = {"data": []}

    iot_manager = initialize_iot_manager()
    connect_future = iot_manager.connect()
    connect_future.result()
    print("Connected!")


    cap = get_capture()
    video_name = create_datetime_video_name()
    writer = create_video_writer(video_name=video_name)

    avg_fps, reading_fps, writing_fps, bohs_fps = initialize_fps_timers()

    count = 0

    bohs_net = BohsNetDetector()

    timeout = get_timeout(2)

    # Camera and detection loop
    # TODO: need to try and break this up a bit.
    #  the FPS counters take up a lot of lines of code... I don't think they need to be used for all ops, such as the cap reading.

    # TODO: split up this block?

    # TODO: *********** More than anything, I need to run this code and see what it looks like rn ***********

    # TODO: Also save the logs within this project, not the PycharmProjects dir!
    try:
        while True:  # I'm not sure if I need this out while True loop. If the cap is opened it should be fine.
            if cap.isOpened():

                print("cap.isOpened:", cap.isOpened())

                while cap.isOpened():

                    # Read the next frame
                    reading_fps.start()
                    ret_val, img = cap.read()
                    reading_fps.stop()

                    # Resize the frame to (720, 1280)
                    img = cv2.resize(img, FRAME_SIZE)

                    if not ret_val:
                        print("Note ret_val. Breaking!")
                        break

                    # Write the frame to the file
                    writing_fps.start()
                    writer.write(img)
                    writing_fps.stop()

                    # Detect the ball
                    bohs_fps.start()
                    dets = bohs_net.detect(img)
                    bohs_fps.stop()

                    dets.update({"bohs_fps": deepcopy(bohs_fps.fps()), "writing_fps": deepcopy(writing_fps.fps()), "reading_fps": deepcopy(reading_fps.fps())})
                    dets = {key: value.tolist() if isinstance(value, Tensor) else value for key, value in dets.items()}
                    json_dict["data"].append(dets)  # We save this file at the end of the match.
                    count+=1

                    # Send the data to the cloud
                    message = json.dumps({
                        "dets": dets,
                        "time": time.time()
                    })
                    iot_manager.publish(payload=message)

                    if time.time() > timeout:
                        print("25 minute timeout")
                        raise KeyboardInterrupt

                    print("Reading FPS:", reading_fps.fps())
                    print("Writing FPS:", writing_fps.fps())
                    print("Bohs FPS:", bohs_fps.fps())
                    print("Frame: ", count)

            else:
                print ("camera open failed")
    except KeyboardInterrupt:
        print("KeyboardInterrupt")

    print("This code is reached")
    cap.release()
    writer.release()
    cv2.destroyAllWindows()
    print("Video saved to", video_name)

    save_to_json_file(json_dict)  # Save json file at the end of the match.
    print("File saved")

    disconnect_future = iot_manager.disconnect()
    disconnect_future.result()
    print("Disconnected!")


def main():
    # Set our file directory
    if DEBUG is False:
        path = "../tim/bohsVids/" + today.strftime('%m_%d_%Y_tim@192.168.73.207')
    else:
        path = "../tim/bohsVids/test"

    check_and_create_dir(path)

    # TODO: we need to add this to our file directory above!
    main_ip_address = get_ip_address()
    print(f"main ip address: {main_ip_address}")

    seconds_till_match = get_seconds_till_match() if DEBUG is False else 1
    print("the match begins in ", seconds_till_match, " seconds")

    _timeout = time.time() + seconds_till_match

    # Going to try to use a while loop instead of a timer
    while time.time() < _timeout:
        print("waiting for match to start")
        time.sleep(1)

    print("Match has started")
    record_and_detect_match_mode()
    print("Match section has ended")

    # Repeat the same process for the second half of the match
    time.sleep(5)
    record_and_detect_match_mode()


if __name__ == '__main__':
    main()
