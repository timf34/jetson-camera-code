import cv2
print(cv2.__version__)

WIDTH: int = 1920
HEIGHT: int = 1080


# This isn't very clean but I am going to keep track of the pipelines that didn't work here for now 
# This wouldn't work. Apparently `nvvidconv` is needed
# cap = cv2.VideoCapture('nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink')


cap = cv2.VideoCapture('nvarguscamerasrc !  video/x-raw(memory:NVMM), width=1920, height=1080, format=NV12, framerate=60/1 ! nvvidconv ! video/x-raw, width='+str(WIDTH)+', height='+str(HEIGHT)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink')


if cap.isOpened():
    print("cap.isOpened:", cap.isOpened())
    cv2.namedWindow("demo", cv2.WINDOW_AUTOSIZE)
    while True:
        ret_val, img = cap.read();
        if not ret_val:
            break
        cv2.imshow('demo',img)
        if cv2.waitKey(1) == ord('q'):
            break
else:
    print ("camera open failed")