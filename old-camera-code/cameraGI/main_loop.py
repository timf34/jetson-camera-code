import threading
import gi 
gi.require_version("Gst", "1.0")
from gi.repository import Gst, GLib
from threading import Thread
from time import sleep 
from datetime import datetime
import os


# Make a new folder for today's videos ---------
today = datetime.now()
path = "/home/tim/bohsVids/" + today.strftime('%m_%d_%Y_tim@192.168.43.53')

if not os.path.isdir(path):
    os.mkdir(path)
    print("the following folder was created: " + path)
else:
    print("The following folder arleady exists: " + path)

# End of folder check --------------------------

# Find the seconds until the beginning of the match for threading Timer

current_time=datetime.today()
time_of_match=current_time.replace(day=current_time.day, hour=15, minute=45, second=40, microsecond=0)
print("current time is ", current_time, "\ntime of the match is ", time_of_match)

delta_t=time_of_match-current_time
seconds_till_match=delta_t.seconds+1
print("the match begins in ", seconds_till_match, " seconds")

# End of finding seconds till match 

# Start of GStreamer code 
Gst.init()

print("ii changed the loop!")
def record_in_batches():

    for i in range(4):
        print("top of loop", datetime.today())
        main_loop = GLib.MainLoop()
        thread = Thread(target=main_loop.run)
        thread.start()

        # pipeline = Gst.parse_launch("nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM),width=1920,height=1080,framerate=30/1 ! nvvidconv ! nvoverlaysink")
        now = datetime.now()
        pipeline = Gst.parse_launch("nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM),width=1920,height=1080,framerate=30/1 ! nvv4l2h264enc ! h264parse ! mp4mux ! filesink location={}/main_test_vid_date_7_11_{}.mp4".format(path, now.strftime("%H_%M_%S")))
        pipeline.set_state(Gst.State.PLAYING)
        if i==2:
            sleep(10)
        else:
            sleep(10)
        pipeline.send_event(Gst.Event.new_eos())
        pipeline.set_state(Gst.State.NULL)
        sleep(5)
        main_loop.quit()
        thread.join()

print("prior to timer t")
t = threading.Timer(seconds_till_match, record_in_batches)
print("prior to t start")
t.start()


