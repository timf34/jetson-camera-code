import cv2
print(cv2.__version__)
dispW=1920
dispH=1080
flip=2

cap = cv2.VideoCapture('nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink')

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