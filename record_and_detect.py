import cv2
import json
import os
import time


from config import BohsConfig
from record_video import VideoRecorder
from utils.fps import FPS
from utils.bohs_net_detector import BohsNetDetector
from utils.utility_funcs import get_ip_address, save_to_json_file, check_and_create_dir


# Inherit from VideoRecorder
class VideoDetector(VideoRecorder):
    def __init__(self, debug: bool = False, width: int = 1280, height: int = 720):
        super().__init__(debug=debug, width=width, height=height)
        self.bohs_net = BohsNetDetector()

    def record_and_detect(self, video_length_mins: float, video_path: str) -> None:
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

        cap.release()
        writer.release()
        cv2.destroyAllWindows()
        print("Video saved to", video_name)

        # TODO: this function has a silly default (cwd + /logs/jetson3 + date_time_file_name.json)
        # save_to_json_file(json_dict)  # Save json file at the end of the match.
        # print("File saved")

        # disconnect_future = iot_manager.disconnect()
        # disconnect_future.result()
        # print("Disconnected!")

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
