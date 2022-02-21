import gi 
from time import sleep 

gi.require_version("Gst", "1.0")

from gi.repository import Gst, GLib
from threading import Thread

Gst.init()


for i in range(5):
    main_loop = GLib.MainLoop()
    thread = Thread(target=main_loop.run)
    thread.start()

    # pipeline = Gst.parse_launch("nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM),width=1920,height=1080,framerate=30/1 ! nvvidconv ! nvoverlaysink")
    pipeline = Gst.parse_launch("nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM),width=1920,height=1080,framerate=30/1 ! nvv4l2h264enc ! h264parse ! mp4mux ! filesink location=main_test_vid_{}.mp4".format(i))
    pipeline.set_state(Gst.State.PLAYING)
    sleep(8)
    pipeline.set_state(Gst.State.NULL)
    main_loop.quit()
    thread.join()
    sleep(10)

