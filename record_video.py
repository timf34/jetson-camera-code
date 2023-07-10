import cv2
import datetime
import os
import time

from datetime import datetime
from typing import Tuple

from config import BohsConfig
from camera_utils.fps import FPS
from camera_utils.logger import Logger
from camera_utils.utility_funcs import get_ip_address, check_and_create_dir, get_log_file_path


class VideoRecorder:
    def __init__(self, debug: bool = False, width: int = 1920, height: int = 1080):
        self.debug: bool = debug
        self.conf: BohsConfig = BohsConfig()
        self.width: int = width
        self.height: int = height
        self.frame_size: Tuple[int, int] = (self.width, self.height)
        self.today: datetime = datetime.now()
        self.jetson_name: str = self.conf.jetson_name[-1]  # The final character of the jetson name (i.e. jetson1 -> 1)
        self.log_file_path: str = get_log_file_path(jetson_name=self.conf.jetson_name)
        self.logger: Logger = Logger(
            log_file_path=self.log_file_path,
            buffer_size=100,
            print_to_console=False,
            console_buffer_size=2
        )
        print(f"Recording resolution: \nWidth: {self.width}\nHeight: {self.height}")


    def get_log_file_path(self):
        """Returns the path to the log file"""
        log_dir = os.path.join(os.getcwd(), 'logs', 'laptop' if os.name == 'nt' else self.jetson_name)
        check_and_create_dir(log_dir)
        return os.path.join(log_dir, f'{self.today.strftime("%d_%m_%Y")}.log')

    def get_seconds_till_match(self):
        """Get the number of seconds till the match starts"""
        current_time = datetime.now()
        match_time = current_time.replace(hour=self.conf.hour, minute=self.conf.minute, second=self.conf.second, microsecond=self.conf.microsecond)
        seconds_till_match = (match_time - current_time).seconds + 1
        if self.debug:
            seconds_till_match = 1
            print("Debug mode is on: seconds till match is 1")
        print(f"get_seconds_till_match()\nCurrent time is {current_time}\nTime of the match is {match_time}\nSeconds till match: {seconds_till_match}")
        return seconds_till_match

    def get_capture(self):
        """Check if the OS is using Windows or Linux and return the correct capture object"""
        if os.name == 'nt':
            return cv2.VideoCapture(0)
        return cv2.VideoCapture(
            f'nvarguscamerasrc !  video/x-raw(memory:NVMM), width=1920, height=1080, format=NV12, framerate=60/1 ! '
            f'nvvidconv ! video/x-raw, width={self.width}, height={self.height}, format=BGRx ! '
            f'videoconvert ! video/x-raw, format=BGR ! appsink'
        )


    def create_video_writer(self, video_name: str) -> cv2.VideoWriter:
        """Create a video writer object"""
        return cv2.VideoWriter(
            filename=video_name,
            fourcc=cv2.VideoWriter_fourcc(*'MJPG'),
            fps=5, 
            frameSize=self.frame_size
        )

    @staticmethod
    def create_datetime_video_name() -> str:
        """Create a video name with the current date and time"""
        now = datetime.now()
        return f"{now.strftime('time_%H_%M_%S_date_%d_%m_%Y_')}.avi"

    @staticmethod
    def initialize_fps_timers() -> Tuple[FPS, FPS, FPS, FPS]:
        """Initialize the FPS timers -> avg_fps, reading_fps, writing_fps, bohs_fps"""
        return FPS(), FPS(), FPS(), FPS()

    def get_timeout(self, timeout_minute_length: float = 22.5) -> int:
        """Return the time in seconds that the video should be recorded for (default is 22.5 minutes)"""
        return int(time.time() + 5 if self.debug else (timeout_minute_length * 60))

    def get_video_path(self) -> str:
        """Return the path to save the video to (doesn't include name!)"""
        if os.name == 'nt':
            return os.path.join('.', 'videos')
        ip_address = get_ip_address()
        video_dir_path = os.path.join('..', 'tim', 'bohsVids', f"{self.today.strftime('%m_%d_%Y@')}_{self.jetson_name}_{ip_address}" if not self.debug else 'test')
        check_and_create_dir(video_dir_path)
        return video_dir_path

    def record_video(self, video_length_mins: float, video_path: str, video_name: str) -> None:
        """
        Record and save a video for as long as set in the timeout

        :param video_length_mins: The length of the video in minutes
        :param video_path: The path to save the video to (i.e. ./videos/) - does not include file name
        """
        cap = self.get_capture()

        full_video_path = os.path.join(video_path, video_name) # Join the path and the name together

        writer = self.create_video_writer(video_name=full_video_path)
        avg_fps, reading_fps, writing_fps, bohs_fps = self.initialize_fps_timers()
        frame_counter = 0
        timeout = self.get_timeout(video_length_mins)

        # Camera loop
        try:
            if cap.isOpened():
                print("Recording video...")
                while cap.isOpened():
                    # Read the next frame
                    reading_fps.start()
                    ret_val, img = cap.read()
                    reading_fps.stop()

                    # Resize the frame to (720, 1280)
                    img = cv2.resize(img, self.frame_size)

                    if not ret_val:
                        print("Not ret_val. Breaking!")
                        break

                    # Write the frame to the file
                    writing_fps.start()
                    writer.write(img)
                    writing_fps.stop()

                    frame_counter += 1

                    if time.time() > timeout:
                        print("Timeout reached. Breaking!")
                        raise KeyboardInterrupt

                    self.logger.log(
                        f"Reading FPS: {reading_fps.fps()} - Writing FPS: {writing_fps.fps()} - Frame: {frame_counter}"
                    )
            else:
                print("Camera not opened")
        except KeyboardInterrupt:
            print("KeyboardInterrupt")

        cap.release()
        writer.release()
        cv2.destroyAllWindows()
        print("Video saved to", video_name)

    @staticmethod
    def wait_for_match_to_start(seconds_till_match: int) -> bool:
        """Waits for the match to start"""
        time_till_match_starts = time.time() + seconds_till_match
        while time.time() < time_till_match_starts:
            print("waiting for match to start")
            time.sleep(3)
        return True

    def record_and_check_video(self, video_length_seconds: int = 5) -> None:
        """Records a quick video and then checks if it's been recorded successfully."""
        video_path = self.get_video_path()
        video_name = self.create_datetime_video_name()

        # Record a quick video
        self.record_video(video_length_seconds/60, video_path, video_name=video_name)

        # Check if the video has been recorded successfully
        full_video_path = os.path.join(video_path, video_name)
        if os.path.isfile(full_video_path):
            print(f"The video has been recorded successfully at {full_video_path}")
        else:
            print(f"The video recording failed. No file at {full_video_path}")
            raise Exception("Video recording failed")

    
    def record_full_match_in_batches(self) -> None:
        """Records videos for the match. Four 22.5-minute long videos + one 10-minute long video for the halftime"""
        # Set our file directory
        path = self.get_video_path()
        check_and_create_dir(path)

        # Record a quick video to check if it's been recorded successfully
        self.record_and_check_video(video_length_seconds=5)

        # Wait for the match to start
        seconds_till_match = self.get_seconds_till_match()
        self.wait_for_match_to_start(seconds_till_match)  # Blocks until the match starts

        num_vids = 1 if self.debug is True else 5 
        for i in range(num_vids):
            if (i == 2) or (i > 5):
                self.record_video(video_length_mins=10, video_path=path, video_name=self.create_datetime_video_name)
            else:
                self.record_video(video_length_mins=22.5, video_path=path, video_name=self.create_datetime_video_name())


def main():
    video_recorder = VideoRecorder(debug=True)
    video_recorder.record_full_match_in_batches()


if __name__ == '__main__':
    main()
