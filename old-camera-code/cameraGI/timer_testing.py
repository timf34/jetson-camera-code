from datetime import datetime, timedelta
import threading
from time import sleep, time 

HOUR = 23 
MIN = 5
SEC = 5
MICRO_SEC = 0

def get_current_time() -> datetime:
    """
    datetime object looks like:
    2022-02-26 22:43:12.310574
    """
    return datetime.today()

def old_code_func():

    current_time = get_current_time()
    print("current time is ", current_time)
    print("its type is,", type(current_time), "\n")

    time_of_match=current_time.replace(day=current_time.day, hour=23, minute=34, second=59, microsecond=0)
    print("time of the match is ", time_of_match, "\n")

    

    # Docs for timedelta object: https://docs.python.org/2/library/datetime.html#timedelta-objects

    delta_t=time_of_match-current_time
    print("delta", delta_t, delta_t.seconds)
    # This returns the TOTAL TIME in seconds
    
    secs=delta_t.seconds+1
    print("there are ", secs, " seconds until the match starts")

    # I left these for the second timer.Threading call below, t2, but I'm not sure why I did it - will just leave this here for now and I can come back and 
    # explore another time.
    # time_of_match_2 = current_time.replace(day=current_time.day, hour=23, minute=43, second=53, microsecond=0)
    # delta_t_2 = time_of_match_2-current_time
    # print("delta t2", delta_t_2, "\n")
    # secs_2=delta_t_2.seconds+1

    def hello_world():
        for i in range(5):
            print("hello world it is: ")
            print(datetime.today())
            sleep(5)
        
    t = threading.Timer(secs, hello_world)
    # t2 = threading.Timer(secs_2, hello_world)
    t.start()
    # t2.start()

    print("this statement comes after t.start() - notice how it executes even though the threading Timer hasn't executed yet!")


def debugging_timer():
    current_time = get_current_time()
    print(current_time.second)


if __name__ == '__main__':
    print("hello world")
    debugging_timer()
    
