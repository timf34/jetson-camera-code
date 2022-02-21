import subprocess

#os.system("sudo gst-launch-1.0 nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM),width=1920,height=1080,framerate=30/1,format=NV12 ! nvv4l2h264enc ! h264parse ! mp4mux ! filesink location=main_test_vid_1.mp4")

# subprocess.call("echo hello", shell=True)

subprocess.call("gst-launch-1.0 -e nvarguscamerasrc sensor-id=0 ! \"video/x-raw(memory:NVMM),width=1920,height=1080,framerate=30/1\" ! nvv4l2h264enc ! h264parse ! mp4mux ! filesink location=main_test_vid_NOW2.mp4", shell=True)
