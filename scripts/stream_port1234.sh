gst-launch-1.0 -ev nvarguscamerasrc ! nvv4l2h264enc insert-vui=1 ! h264parse ! rtph264pay config-interval=1 pt=96 ! udpsink host=192.168.141.1 port=1234 

# Change the IP address above to 192.168.118.141 if I'm on 5GHz I think 
# in the file above, host must equal the IP adress of your laptop!!!
