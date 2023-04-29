"""
This file contains a function that resets the GStreamer pipeline.
This is useful when you want to restart the GStreamer pipeline
without turning the Jetson off and on again (i.e. in case we
get a memory leak error or such when shutting down a GStreamer
pipeline).

Run this file with sudo privileges (i.e. `sudo python3 gstreamer_resetting.py`)
"""

import subprocess

def reset_gstreamer_pipeline():
    try:
        subprocess.run(["sudo", "fuser", "-k", "/dev/video0"], check=True)
        print("GStreamer pipeline reset successfully")
    except subprocess.CalledProcessError as e:
        print("Failed to reset GStreamer pipeline:", e)

# Call this function whenever you want to reset the GStreamer pipeline.
reset_gstreamer_pipeline()
