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
                         60, FRAME_SIZE)
count = 0 
if cap.isOpened():
    print("cap.isOpened:", cap.isOpened())
    # cv2.namedWindow("demo", cv2.WINDOW_AUTOSIZE)
    while True:
        ret_val, img = cap.read();
        if not ret_val:
            break
        # cv2.imshow('demo',img)
        writer.write(img)
        print(count)
        count+=1
        # if cv2.waitKey(1) == ord('q'):
        #    break
else:
    print ("camera open failed")

cap.release()
writer.release()