gst-launch-1.0 -ev nvarguscamerasrc ! nvv4l2h264enc insert-vui=1 ! h264parse ! rtph264pay config-interval=1 pt=96 ! udpsink host=192.168.43.220 port=1234 
