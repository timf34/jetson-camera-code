import gi 
from time import sleep 
from datetime import datetime
import os

# Make a new folder for today's videos 
today = datetime.now()

path = "/home/tim/bohsVids/" + today.strftime('%m_%d_%Y_tim@192.168.43.53')

if not os.path.isdir(path):
    os.mkdir(path)
else:
    print("it exists")


gi.require_version("Gst", "1.0")

from gi.repository import Gst, GLib
from threading import Thread

Gst.init()


main_loop = GLib.MainLoop()
thread = Thread(target=main_loop.run)
thread.start()

# pipeline = Gst.parse_launch("nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM),width=1920,height=1080,framerate=30/1 ! nvvidconv ! nvoverlaysink")
pipeline = Gst.parse_launch("nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM),width=1920,height=1080,framerate=30/1 ! nvv4l2h264enc ! h264parse ! mp4mux ! filesink location={}/main_test_vid_oiuk.mp4".format(path))
pipeline.set_state(Gst.State.PLAYING)
sleep(5)
pipeline.send_event(Gst.Event.new_eos())
pipeline.set_state(Gst.State.NULL)
sleep(5)
main_loop.quit()
thread.join()
