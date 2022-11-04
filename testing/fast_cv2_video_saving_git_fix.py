"""
This file uses multi-threading to save video frames to a video file at a faster speed. 
"""

import cv2
import time  # for timing
import numpy as np
import threading

print(cv2.__version__)

WIDTH: int = 1920
HEIGHT: int = 1080
FRAME_SIZE = (WIDTH, HEIGHT)

FPS: int = 60


def get_cam():
    """
    This function gets the camera and returns it.
    """
    return cv2.VideoCapture('nvarguscamerasrc !  video/x-raw(memory:NVMM), width=1920, height=1080, format=NV12, '
                            'framerate=60/1 ! nvvidconv ! video/x-raw, width='+str(WIDTH)+', height='+str(HEIGHT)+', '
                            'format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink')


def get_writer():
    """
    This function gets the writer and returns it.
    """
    return cv2.VideoWriter('filename.avi',
                          cv2.VideoWriter_fourcc(*'MJPG'),
                          FPS, FRAME_SIZE)


def get_frame(cam):
    """
    This function gets a frame from the camera and returns it.
    """
    ret_val, img = cam.read()
    return img


def save_frame(writer, frame):
    """
    This function saves a frame to the video file.
    """
    writer.write(frame)


def main():
    """
    This function runs the main program. 
    It uses multithreading to save the frames to a video file faster
    """
    cam = get_cam()
    writer = get_writer()
    
    # start the timer
    start = time.time()
    count = 0
    
    # create a list of threads
    threads = []
    
    # create a thread for each frame
    for i in range(3):
        t = threading.Thread(target=save_frame, args=(writer, get_frame(cam)))
        threads.append(t)
        t.start()
    
    # wait for all threads to finish
    for t in threads:
        t.join()
        
    # stop the timer
    end = time.time()
    print("Time:", end - start)
    print("Frames:", count)
    print("FPS:", count / (end - start))
    
    # release the camera
    cam.release()
    writer.release()
    

if __name__ == '__main__':
    main()
    
    
