from datetime import datetime 
import socket
import subprocess

def time_func():

    now = datetime.now() # current date and time

    time = now.strftime("%H_%M_%S")

    print(time)

    day_month_year = now.strftime("%d_%m_%Y")
    print(day_month_year)

def get_ip_address():
    """
        Returns string - function annotations/ typing does weird stuff to code editor colours...?
    """
    # IP address 
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print("The main IP address", s.getsockname()[0])
    global_ip_address = s.getsockname()[0]
    return global_ip_address


def subprocess_log():
    pass


if __name__ == '__main__':
    pass