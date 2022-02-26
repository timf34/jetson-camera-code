from datetime import datetime
import os
import socket

today = datetime.now()

path = "/home/tim/bohsVids/" + today.strftime('%m_%d_%Y_tim@192.168.73.207')

if not os.path.isdir(path):
    os.mkdir(path)
    print("Here is the new path:", path)
else:
    print("The path already exists:", path)


# Getting the IP address:)
# Source: https://www.delftstack.com/howto/python/get-ip-address-python/

# This just gets the local IP address 
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

print("hostname:", hostname, "\nlocal_ip:", local_ip)

# IP address that I care about - the identifying one:) 
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print("The main IP address", s.getsockname()[0])



def get_global_variables():
    global global_today, ip_address
    # Lets get some of our variables for our folders
    # date/time object 
    global_today = datetime.now()

    # IP address 
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print("The main IP address", s.getsockname()[0])
    ip_address = s.getsockname()[0]


if __name__ == '__main__':
    get_global_variables()

    print("ip is here:", ip_address)