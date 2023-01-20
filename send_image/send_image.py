import paramiko
import subprocess

# GStreamer pipeline to capture and send the image
# This pipeline takes and image. It uses multifilesinks to take multiple images to allow auto-tune to warm up; we only take the last one with a time buffer of 1,000,000 nanoseconds (1 second).
# Note that the early timeout is crucial in getting the stream to turn off.
pipeline = "gst-launch-1.0 nvarguscamerasrc sensor_id=0 timeout=10 ! \"video/x-raw(memory:NVMM), width=1920, height=1080, framerate=60/1\" ! nvjpegenc ! multifilesink location=test_yolo.jpg max-files=1 max-file-duration=1000000000"

# # Run the pipeline
# subprocess.run(pipeline)

# pipeline = "echo \"hello world\""

subprocess.run(pipeline, shell=True)


# Send the image to our laptop