from fps import FPS
import cv2
print(cv2.__version__)

WIDTH: int = 1920
HEIGHT: int = 1080

FRAME_SIZE = (WIDTH, HEIGHT)


# This isn't very clean but I am going to keep track of the pipelines that didn't work here for now 
# This wouldn't work. Apparently `nvvidconv` is needed
# cap = cv2.VideoCapture('nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink')


cap = cv2.VideoCapture('nvarguscamerasrc !  video/x-raw(memory:NVMM), width=1920, height=1080, format=NV12, framerate=60/1 ! nvvidconv ! video/x-raw, width='+str(WIDTH)+', height='+str(HEIGHT)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink')

# so with this setup, its way too slow, not close to 60fps, I'm gonna try it with another
# ... I was about to say that I was going to try it with thie filesink but that miight make things difficult with the
# threads... probably best to just leave this for tmrw for now 
writer = cv2.VideoWriter('filename.avi',
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         5, FRAME_SIZE)

avg_fps = FPS()
reading_fps = FPS()
writing_fps = FPS()

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

                # cv2.imshow('demo',img)

                # Write the frame to the file
                writing_fps.start()
                writer.write(img)
                writing_fps.stop()
                avg_fps.update()

                # Exit if any key is pressed
                print("prio")
                key = cv2.waitKey(25)
                print("jere os tje leu", key)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        else:
            print ("camera open failed")
except KeyboardInterrupt:
    print("KeyboardInterrupt")
    avg_fps.stop()
    print("Average FPS:", avg_fps.average_fps())
    print("Reading FPS:", reading_fps.fps())
    print("Writing FPS:", writing_fps.fps())
    cap.release()
    writer.release()
    pass

print("we made it out here")