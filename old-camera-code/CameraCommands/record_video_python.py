import cv2

print("cv2 version:", cv2.__version__)

# camSet = "nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM),width=1920,height=1080,framerate=30/1,format=NV12 ! nvv4l2h264enc ! h264parse ! mp4mux ! filesink location=main_test_vid_$NOW.mp4 "
# camSet = 'nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM),width=1920,height=1080,framerate=30/1 ! nvidconv flip-method=2 ! video/x-raw, width=800, height=600, BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
camSet = "nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM), width=1920, height=1080, format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink"

cam = cv2.VideoCapture(camSet, cv2.CAP_GSTREAMER)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('test1.avi', fourcc, 30.0, (1920, 1080))

if cam.isOpened():
    while True:
        _, frame = cam.read()
        cv2.imshow('myCam', frame)
        out.write(frame)
        if cv2.waitKey(1)==ord('q'):
            break

out.release()
cam.release()
cv2.destroyAllWindows()
