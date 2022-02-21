from datetime import datetime
import threading
from time import sleep 

current_time=datetime.today()
time_of_match=current_time.replace(day=current_time.day, hour=13, minute=34, second=59, microsecond=0)
time_of_match_2 = current_time.replace(day=current_time.day, hour=13, minute=43, second=53, microsecond=0)

delta_t=time_of_match-current_time
delta_t_2 = time_of_match_2-current_time

print("current time is ", current_time)
print("time of the match is ", time_of_match)

secs=delta_t.seconds+1
secs_2=delta_t_2.seconds+1
print("there are ", secs, " seconds until the match starts")

def hello_world():
    for i in range(5):
        print("hello world it is: ")
        print(datetime.today())
        sleep(5)
    
t = threading.Timer(secs, hello_world)
# t2 = threading.Timer(secs_2, hello_world)
t.start()
# t2.start()

print("this statement comes after t.start()")