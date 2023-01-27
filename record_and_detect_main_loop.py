import cv2
import datetime
import os
import time


from copy import deepcopy
from datetime import datetime
from torch import Tensor as Tensor
from typing import Tuple

from config import BohsConfig
from utils.fps import FPS
from utils.bohs_net_detector import BohsNetDetector
from utils.utility_funcs import get_ip_address, save_to_json_file


# Constants
DEBUG = False
CURRENT_TIME = datetime.now() # not sure if this is bad practice but it works
WIDTH: int = 1280
HEIGHT: int = 720
FRAME_SIZE = (WIDTH, HEIGHT)
today = datetime.now()
conf = BohsConfig()


def get_seconds_till_match():
    """
    This function finds the difference in time (in seconds) beteween the current time, and the time of the match 

    returns int
    """
    current_time = datetime.now()
    time_of_match = current_time.replace(day=current_time.day,
                                       hour=conf.hour,
                                       minute=conf.minute,
                                       second=conf.second,
                                       microsecond=conf.microsecond)
    delta_t = time_of_match-current_time

    print("current time is ", current_time, "\ntime of the match is ", time_of_match)
    return delta_t.seconds+1


def get_capture():
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


def record_and_detect_match_mode():
    
    # Initialization
    json_dict = {"data": []}

    cap = get_capture()
    video_name = create_datetime_video_name()
    writer = create_video_writer(video_name=video_name)

    avg_fps, reading_fps, writing_fps, bohs_fps = initialize_fps_timers()

    count = 0

    bohs_net = BohsNetDetector()

    ONE_MIN_TIMEOUT = time.time() + 60  # 1 minute from now
    TWO_MIN_TIMEOUT = time.time() + 120  # 2 minutes from now
    THREE_MIN_TIMEOUT = time.time() + 180  # 3 minutes from now
    FIVE_MIN_TIMEOUT = time.time() + 300  # 5 minutes from now
    TWENTYTWO_5_MIN_TIMEOUT = time.time() + 1350  # 22.5 minutes from now

    # Camera and detection loop
    try:
        while True:
            if cap.isOpened():

                print("cap.isOpened:", cap.isOpened())

                avg_fps.start()

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
                    print("Writing frame")
                    writer.write(img)
                    writing_fps.stop()
                    avg_fps.update()

                    # Detect the ball
                    bohs_fps.start()
                    print("Ball detection")
                    dets = bohs_net.detect(img)
                    bohs_fps.stop()
                    dets.update({"bohs_fps": deepcopy(bohs_fps.fps()), "writing_fps": deepcopy(writing_fps.fps()), "reading_fps": deepcopy(reading_fps.fps())})
                    dets = {key: value.tolist() if isinstance(value, Tensor) else value for key, value in dets.items()}
                    json_dict["data"].append(dets)
                    count+=1

                    if time.time() > TWENTYTWO_5_MIN_TIMEOUT:
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

    print("Now lets save json_dict to a file")
    save_to_json_file(json_dict)
    print("File saved")


if __name__ == '__main__':
    
    # Set our file directory 
    if DEBUG is False: 
        path = "../tim/bohsVids/" + today.strftime('%m_%d_%Y_tim@192.168.73.207')
    else:
        path = "../tim/bohsVids/test"


    # Check if directory exists, else create a new one
    if not os.path.isdir(path):	
        os.makedirs(path)
        print(f"the following folder was created: {path}")
    else:
        print(f"The following folder arleady exists: {path}")

    # Print IP address
    # TODO: we need to add this to our file directory above!
    main_ip_address = get_ip_address()
    print("main ip address: ")

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


