import paramiko
import subprocess
from time import sleep

from windows_config import PASSWORD

# This pipeline takes and image. It uses multifilesinks to take multiple images to allow auto-tune to warm up; we only take the last one with a time buffer of 1,000,000 nanoseconds (1 second).
# Note that the early timeout is crucial in getting the stream to turn off.
# pipeline = "gst-launch-1.0 nvarguscamerasrc sensor_id=0 timeout=10 ! \"video/x-raw(memory:NVMM), width=1920, height=1080, framerate=60/1\" ! nvjpegenc ! multifilesink location=test_yolo2.jpg max-files=1 max-file-duration=1000000000"


class SendImage:
    def __init__(self):
        self.image_name: str = 'test_yolo.jpg'
        self.pipeline: str = f"gst-launch-1.0 nvarguscamerasrc sensor_id=0 timeout=10 ! \"video/x-raw(memory:NVMM), width=1920, height=1080, framerate=60/1\" ! nvjpegenc ! multifilesink location={self.image_name} max-files=1 max-file-duration=1000000000"

        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.laptop_ipv4_address: str = '192.168.84.1'
        self.laptop_username: str = 'timf34/timf3'  # found via `whoami` on the windows machine
        self.laptop_password: str = PASSWORD

        # Send the file. Note that the target path needs to be to a file - a directory won't work!
        self.target_file: str = 'C:/Users/timf3/Downloads/test_yolo.jpg'

    def capture_image(self) -> None:
        subprocess.run(self.pipeline, shell=True)
        sleep(3)  # Wait for the image to be saved

    def send_image(self) -> None:
        self.client.connect(self.laptop_ipv4_address, username=self.laptop_username, password=self.laptop_password)
        sftp = self.client.open_sftp()
        sftp.put(self.image_name, self.target_file)
        sftp.close()
        self.client.close()


if __name__ == '__main__':
    send_image = SendImage()
    send_image.capture_image()
    send_image.send_image()