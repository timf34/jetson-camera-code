import socket

def get_ip_address():
    """
        Returns string - function annotations/ typing does weird stuff to code editor colours...?
    """
    # IP address 
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    # print("The main IP address", s.getsockname()[0])
    return s.getsockname()[0]
