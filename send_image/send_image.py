import paramiko
import subprocess

from windows_config import PASSWORD

# GStreamer pipeline to capture and send the image
# This pipeline takes and image. It uses multifilesinks to take multiple images to allow auto-tune to warm up; we only take the last one with a time buffer of 1,000,000 nanoseconds (1 second).
# Note that the early timeout is crucial in getting the stream to turn off.
# pipeline = "gst-launch-1.0 nvarguscamerasrc sensor_id=0 timeout=10 ! \"video/x-raw(memory:NVMM), width=1920, height=1080, framerate=60/1\" ! nvjpegenc ! multifilesink location=test_yolo.jpg max-files=1 max-file-duration=1000000000"

# # # Run the pipeline
# subprocess.run(pipeline, shell=True)


# Send the image to our laptop
# Set up the SSH client
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the Windows machine
# Connect to the Windows machine
client.connect(hostname='192.168.84.1', username='timf34/timf3', password=PASSWORD)

# Open a SFTP session
sftp = client.open_sftp()

# Send the file. Note that the target path needs to be to a file - a directory won't work!
sftp.put('test_yolo.jpg', 'C:/Users/timf3/Downloads/test_yolo.jpg')

# Close the SFTP session and SSH client
sftp.close()
client.close()
