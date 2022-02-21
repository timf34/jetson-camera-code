SENSOR_ID=0 # 0 for CAM0 and 1 for CAM1 ports
FRAMERATE=30
NUMBER_OF_SNAPSHOTS=30
NOW=$( date '+%F_%H:%M:%S' )
gst-launch-1.0 -e nvarguscamerasrc num-buffers=$NUMBER_OF_SNAPSHOTS sensor-id=$SENSOR_ID ! "video/x-raw(memory:NVMM),width=1920,height=1080,framerate=$FRAMERATE/1" ! nvjpegenc ! multifilesink location=test_image_$NOW.jpeg
gst-launch-1.0 -e nvarguscamerasrc sensor-id=$SENSOR_ID ! "video/x-raw(memory:NVMM),width=1920,height=1080,framerate=$FRAMERATE/1" ! nvv4l2h264enc ! h264parse ! mp4mux ! filesink location=main_test_vid_$NOW.mp4 
