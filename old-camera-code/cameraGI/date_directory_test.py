from datetime import datetime
import os

today = datetime.now()

path = "/home/tim/bohsVids/" + today.strftime('%m_%d_%Y_tim@192.168.43.53')

if not os.path.isdir(path):
    os.mkdir(path)
else:
    print("it exists")


