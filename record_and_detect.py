from fps import FPS
from bohs_net_detector import BohsNetDetector

import cv2
print(cv2.__version__)

WIDTH: int = 1920
HEIGHT: int = 1080

FRAME_SIZE = (WIDTH, HEIGHT)


# This isn't very clean but I am going to keep track of the pipelines that didn't work here for now 
# This wouldn't work. Apparently `nvvidconv` is needed
# cap = cv2.VideoCapture('nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink')


cap = cv2.VideoCapture('nvarguscamerasrc !  video/x-raw(memory:NVMM), width=1920, height=1080, format=NV12, framerate=60/1 ! nvvidconv ! video/x-raw, width='+str(WIDTH)+', height='+str(HEIGHT)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink')

writer = cv2.VideoWriter('filename.avi',
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         5, FRAME_SIZE)

avg_fps = FPS()
reading_fps = FPS()
writing_fps = FPS()

bohs_net = BohsNetDetector()

try:
    while True:
        if cap.isOpened():

            print("cap.isOpened:", cap.isOpened())

            avg_fps.start()

            while True:

                # Read the next frame
                reading_fps.start()
                ret_val, img = cap.read();
                reading_fps.stop()

                if not ret_val:
                    break

                # Write the frame to the file
                writing_fps.start()
                writer.write(img)
                writing_fps.stop()
                avg_fps.update()

                # Detect the ball
                bohs_net.detect_ball(img)

                # Exit if any key is pressed
                print("Reading FPS:", reading_fps.fps())
                print("Writing FPS:", writing_fps.fps())

        else:
            print ("camera open failed")
except KeyboardInterrupt:
    print("KeyboardInterrupt")

print("This code is reached")
cap.release()
writer.release()
avg_fps.stop()
print("Average FPS:", avg_fps.average_fps())