from re import X
import threading
import gi 
gi.require_version("Gst", "1.0")
from gi.repository import Gst, GLib
from threading import Thread
from time import sleep 
from datetime import datetime
import socket
import os
import sys 
# TODO: I should look more into threading.Timer and the best way to use!
# TODO: look into subprocess more! It will be useful for looging all the output from the terminal it seems 


DEBUG = False
CURRENT_TIME = datetime.now() # not sure if this is bad practice but it works
# sys.stdout = open("test123.txt", "w")
# This isn't what I want for Bohs where I want to see output! This redirects all console output besides that from the nvargus (which is different somehow)

# This might as well be a global constant
today = datetime.now()
    

# TODO: I need a flag for entering test or debug mode! And to change directory accordingly. And we can make it so that I default to normal mode:)
#  it might also be a good idea for me to use flags/ the command line to enter the time of the match, or to confirm it.


def get_ip_address():
    """
        Returns string - function annotations/ typing does weird stuff to code editor colours...?
    """
    # IP address 
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    # print("The main IP address", s.getsockname()[0])
    return s.getsockname()[0]
    

def get_seconds_till_match():
    """
    This function finds the difference in time (in seconds) beteween the current time, and the time of the match 

    returns int
    """
    current_time=datetime.today()
    time_of_match=current_time.replace(day=current_time.day, hour=18, minute=01, second=1, microsecond=0)
    delta_t=time_of_match-current_time
     
    print("current time is ", current_time, "\ntime of the match is ", time_of_match) 
    return delta_t.seconds+1  


# TODO: I should change the below funcitons into one function, and just pass the relevant variables through.
def record_in_batches_match_mode():

    # It goes 0, 1, 2 - where 0 and 2 are the 1st and 2nd halfs, and i=1 is halftime 
    for i in range(4):
        print("top of loop", datetime.today())
        main_loop = GLib.MainLoop()
        thread = Thread(target=main_loop.run)
        thread.start()

        # pipeline = Gst.parse_launch("nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM),width=1920,height=1080,framerate=30/1 ! nvvidconv ! nvoverlaysink")
        now = datetime.now()
        pipeline = Gst.parse_launch("nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM),width=1920,height=1080,framerate=60/1 ! nvv4l2h264enc ! h264parse ! mp4mux ! filesink location={}/jetson1_date:{}_time:_{}.mp4".format(path, now.strftime("%d_%m_%Y"), now.strftime("%H_%M_%S")))
        pipeline.set_state(Gst.State.PLAYING)
        if i==1 or i==3:
            # This is for halftime, plus extra time in case 
            sleep(600)
        else:
            # 60 x 45 = 2700 seconds for each halftime 
            sleep(2700)
        pipeline.send_event(Gst.Event.new_eos())
        pipeline.set_state(Gst.State.NULL)
        sleep(5)
        main_loop.quit()
        thread.join()



def record_test_mode():
    for i in range(3):
        print("top of loop", datetime.today())
        main_loop = GLib.MainLoop()
        thread = Thread(target=main_loop.run)
        thread.start()

        # pipeline = Gst.parse_launch("nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM),width=1920,height=1080,framerate=30/1 ! nvvidconv ! nvoverlaysink")
        now = datetime.now()
        pipeline = Gst.parse_launch("nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM),width=1920,height=1080,framerate=60/1 ! nvv4l2h264enc ! h264parse ! mp4mux ! filesink location={}/test_date:{}_time:_{}.mp4".format(path, now.strftime("%d_%m_%Y"), now.strftime("%H_%M_%S")))
        pipeline.set_state(Gst.State.PLAYING)
        # This is use waiting for the 
        if i==1:
            sleep(10)
        else:
            sleep(5)
        pipeline.send_event(Gst.Event.new_eos())
        pipeline.set_state(Gst.State.NULL)
        sleep(5)
        main_loop.quit()
        thread.join()




if __name__ == '__main__':
    
    # Set our file directory 
    if DEBUG is False: 
        path = "../tim/bohsVids/" + today.strftime('%m_%d_%Y_tim@192.168.73.207')
    else:
        path = "../tim/bohsVids/test"


    # Check if directory exists, else create a new one
    if not os.path.isdir(path):	
        os.makedirs(path)
        print("the following folder was created: " + path)
    else:
        print("The following folder arleady exists: " + path)

    # Print IP address 
    # TODO: we need to add this to our file directory above!
    main_ip_address = get_ip_address()
    print("main ip address: ")

    if DEBUG is False:      
    # Find the difference between the current time, and the time of the match - this will set our timer 
        seconds_till_match = get_seconds_till_match()
    else:
        seconds_till_match = 1 # for debugging we have this setup so it starts basically instantly
        

    print("the match begins in ", seconds_till_match, " seconds")

    # Start of GStreamer code 
    Gst.init()

    print("prior to timer t")
    if DEBUG is False: 
        t = threading.Timer(seconds_till_match, record_in_batches_match_mode)
    else:
        t = threading.Timer(seconds_till_match, record_test_mode)
        
    print("prior to t start")
    t.start()
