import subprocess

# GStreamer pipeline to capture and send the image
# This pipeline takes and image. It uses multifilesinks to take multiple images to allow auto-tune to warm up; we only take the last one with a time buffer of 1,000,000 nanoseconds (1 second).
pipeline = "gst-launch-1.0 nvarguscamearsrc sensor_id=0\" ! \"video/x-raw(memory:NVMM), width=1920, height=1080, framerate=60/1\" ! nvjpegenc ! multifilesink location=test_yolo.jpg max-files=1 max-file-duration=1000000000"

# Run the pipeline
subprocess.call(pipeline, shell=True)