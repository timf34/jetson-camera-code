import cv2
import json
import os
import time

from torch import Tensor
from typing import Dict

from config import BohsConfig
from record_video import VideoRecorder
from camera_utils.bohs_net_detector import BohsNetDetector
from camera_utils.fps import FPS
from camera_utils.logger import Logger
from camera_utils.utility_funcs import get_log_file_path, check_and_create_dir, get_aws_iot_manager


# TODO: I might want to extend the iot_manager class to set a longer timeout/ keepalive value
class VideoDetector(VideoRecorder):
    def __init__(self, debug: bool = False, width: int = 1280, height: int = 720):
        super().__init__(debug=debug, width=width, height=height)
        self.config: BohsConfig = BohsConfig()
        self.bohs_net: BohsNetDetector = BohsNetDetector()
        self.log_file_path: str = get_log_file_path(jetson_name=self.config.jetson_name)
        self.logger: Logger = Logger(
            log_file_path=self.log_file_path,
            buffer_size=100,
            print_to_console=True,
            console_buffer_size=2
        )
        self.iot_manager = get_aws_iot_manager(self.config)

    @staticmethod
    def convert_det_tensor_to_dict(det_tensor: Dict[str, Tensor]) -> Dict[str, Tensor]:
        """Converts our detection dict with tensor to a dict with list"""
        print(det_tensor)
        return {key: value.tolist() if isinstance(value, Tensor) else value for key, value in det_tensor.items()}

    def record_and_detect(self, video_length_mins: float, video_path: str) -> None:
        """
        Record and save a video for as long as set in the timeout; also perform ball detection

        :param video_length_mins: The length of the video in minutes
        :param video_path: The path to save the video to (i.e. ./videos/) - does not include file name
        """
        # json_dict = {"data": []}
        cap = self.get_capture()

        video_name = self.create_datetime_video_name()
        video_path = os.path.join(video_path, video_name)

        writer = self.create_video_writer(video_name=video_path)
        avg_fps, reading_fps, writing_fps, bohs_fps = self.initialize_fps_timers()
        frame_counter = 0
        timeout = self.get_timeout(video_length_mins)

        self.iot_manager.connect()

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
                    dets = {key: value.tolist() if isinstance(value, Tensor) else value for key, value in dets.items()}
                    # json_dict["data"].append(dets)  # We save this file at the end of the match.
                    #
                    # # Send the data to the cloud
                    aws_message = json.dumps({
                        "dets": dets,
                        "time": time.time(),
                        "camera": self.jetson_name
                    })
                    self.iot_manager.publish(payload=aws_message)

                    self.logger.log(aws_message)

                    if time.time() > timeout:
                        print("25 minute timeout")
                        raise KeyboardInterrupt

                    self.logger.log(
                        f"Reading FPS: {reading_fps.fps()} - Writing FPS: {writing_fps.fps()} - "
                        f"Bohs FPS: {bohs_fps.fps()} - Frame: {frame_counter}"
                    )
            else:
                print("camera open failed")
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
        finally:
            cap.release()
            writer.release()
            print("Video saved to", video_name)

        # TODO: this function has a silly default (cwd + /logs/jetson3 + date_time_file_name.json)
        # save_to_json_file(json_dict)  # Save json file at the end of the match.
        self.iot_manager.disconnect()

    def record_and_detect_full_match_in_batches(self) -> None:
        """
        Records videos + does ball detection for the full match in batches of 22.5-minutes + one 10-minute batch
        for halftime
        """
        path = self.get_video_path()
        check_and_create_dir(path)

        seconds_till_match = self.get_seconds_till_match()
        self.wait_for_match_to_start(seconds_till_match)

        for i in range(5):
            if (i == 2) or (i > 5):
                self.record_and_detect(video_length_mins=10, video_path=path)
            else:
                self.record_and_detect(video_length_mins=22.5, video_path=path)


if __name__ == '__main__':
    video_detector = VideoDetector(debug=True)
    video_detector.record_and_detect_full_match_in_batches()
