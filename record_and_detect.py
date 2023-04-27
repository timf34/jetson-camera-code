import cv2
import json
import os
import time

from copy import deepcopy
from torch import Tensor as Tensor
from typing import Tuple

from config import BohsConfig
from utils.fps import FPS
from utils.bohs_net_detector import BohsNetDetector
from utils.utility_funcs import get_ip_address, save_to_json_file, check_and_create_dir

from fov_net.camera_send_messages import initialize_iot_manager

from record_video import VideoRecorder


# Inherit from VideoRecorder
class VideoDetector(VideoRecorder):
    def __init__(self, debug: bool = False, width: int = 1280, height: int = 720):
        super().__init__(debug=debug, width=width, height=height)
        self.bohs_net = BohsNetDetector()

    def record_and_detect_match_mode(self, video_length_mins: float, video_path: str) -> None:
        """
        Record and save a video for as long as set in the timeout; also perform ball detection

        :param video_length_mins: The length of the video in minutes
        :param video_path: The path to save the video to (i.e. ./videos/) - does not include file name
        """
        json_dict = {"data": []}
        cap = self.get_capture()

        video_name = self.create_datetime_video_name()
        video_path = os.path.join(video_path, video_name)

        writer = self.create_video_writer(video_name=video_path)
        avg_fps, reading_fps, writing_fps, bohs_fps = self.initialize_fps_timers()
        frame_counter = 0
        timeout = self.get_timeout(video_length_mins)

        # iot_manager = initialize_iot_manager()
        # connect_future = iot_manager.connect()
        # connect_future.result()

        try:
            if cap.isOpened():
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

                    # Detect the ball
                    bohs_fps.start()
                    dets = self.bohs_net.detect(img)
                    bohs_fps.stop()

                    # dets.update({"bohs_fps": deepcopy(bohs_fps.fps()), "writing_fps": deepcopy(writing_fps.fps()),
                    #              "reading_fps": deepcopy(reading_fps.fps())})
                    # dets = {key: value.tolist() if isinstance(value, Tensor) else value for key, value in dets.items()}
                    # json_dict["data"].append(dets)  # We save this file at the end of the match.
                    #
                    # # Send the data to the cloud
                    # message = json.dumps({
                    #     "dets": dets,
                    #     "time": time.time(),
                    #     "camera": self.jetson_name
                    # })
                    # iot_manager.publish(payload=message)

                    if time.time() > timeout:
                        print("25 minute timeout")
                        raise KeyboardInterrupt

                    print("Reading FPS:", reading_fps.fps())
                    print("Writing FPS:", writing_fps.fps())
                    print("Bohs FPS:", bohs_fps.fps())
                    print("Frame: ", frame_counter)

            else:
                print("camera open failed")
        except KeyboardInterrupt:
            print("KeyboardInterrupt")

        print("This code is reached")
        cap.release()
        writer.release()
        cv2.destroyAllWindows()
        print("Video saved to", video_name)

        save_to_json_file(json_dict)  # Save json file at the end of the match.
        print("File saved")

        # disconnect_future = iot_manager.disconnect()
        # disconnect_future.result()
        # print("Disconnected!")


    def main(self):
        # Set our file directory
        if self.debug is False:
            path = "../tim/bohsVids/" + self.today.strftime('%m_%d_%Y_tim@192.168.73.207')
        else:
            path = "../tim/bohsVids/test"

        check_and_create_dir(path)

        # TODO: we need to add this to our file directory above!
        main_ip_address = get_ip_address()
        print(f"main ip address: {main_ip_address}")

        seconds_till_match = self.get_seconds_till_match() if self.debug is False else 1
        print("the match begins in ", seconds_till_match, " seconds")

        _timeout = time.time() + seconds_till_match

        # Going to try to use a while loop instead of a timer
        while time.time() < _timeout:
            print("waiting for match to start")
            time.sleep(1)

        print("Match has started")
        self.record_and_detect_match_mode()
        print("Match section has ended")

        # Repeat the same process for the second half of the match
        time.sleep(5)
        self.record_and_detect_match_mode()


if __name__ == '__main__':
    video_detector = VideoDetector(debug=True)
    video_detector.main()

