from datetime import datetime 


now = datetime.now() # current date and time

time = now.strftime("%H_%M_%S")

print(time)