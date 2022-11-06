import cv2
import json
import os
import time 
from torch import Tensor as Tensor

from copy import deepcopy
from typing import Dict, List

from fps import FPS
from bohs_net_detector import BohsNetDetector

print(cv2.__version__)

WIDTH: int = 1280
HEIGHT: int = 720

FRAME_SIZE = (WIDTH, HEIGHT)


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


def main():

    # This isn't very clean but I am going to keep track of the pipelines that didn't work here for now 
    # This wouldn't work. Apparently `nvvidconv` is needed
    # cap = cv2.VideoCapture('nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink')

    json_dict = {"data": []}

    cap = cv2.VideoCapture('nvarguscamerasrc !  video/x-raw(memory:NVMM), width=1920, height=1080, format=NV12, framerate=60/1 ! nvvidconv ! video/x-raw, width='+str(WIDTH)+', height='+str(HEIGHT)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink')

    # For working on my laptop
    # cap = cv2.VideoCapture(0)

    writer = cv2.VideoWriter('filename.avi',
                            cv2.VideoWriter_fourcc(*'MJPG'),
                            5, FRAME_SIZE)

    avg_fps = FPS()
    reading_fps = FPS()
    writing_fps = FPS()
    bohs_fps = FPS()

    count = 0

    bohs_net = BohsNetDetector()

    try:
        while True:
            if cap.isOpened():

                print("cap.isOpened:", cap.isOpened())

                avg_fps.start()

                while cap.isOpened():

                    # Read the next frame
                    reading_fps.start()
                    print("Reading frame")
                    ret_val, img = cap.read()
                    reading_fps.stop()

                    # Resize the frame to (720, 1280)
                    img = cv2.resize(img, FRAME_SIZE)

                    if not ret_val:
                        print("Breaking!")
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

                    # Exit if any key is pressed
                    # print("Reading FPS:", reading_fps.fps())
                    # print("Writing FPS:", writing_fps.fps())
                    # print("Bohs FPS:", bohs_fps.fps())
                    # print("Frame: ", count)

            else:
                print ("camera open failed")
    except KeyboardInterrupt:
        print("KeyboardInterrupt")

    print("This code is reached")
    cap.release()
    writer.release()
    avg_fps.stop()
    print("Average FPS:", avg_fps.average_fps())

    print("Now lets save json_dict to a file")
    save_to_json_file(json_dict)
    print("File saved")


if __name__ == '__main__':
    main()
