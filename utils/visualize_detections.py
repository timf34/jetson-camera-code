import cv2
import json

from dataclasses import dataclass
from typing import List, Dict, Iterator

"""
    Plan:
        - Write function to parse the Json file 
        - Run through the json file (can create an iterator) and video frame by frame, and draw a box if there's a detection. 
        - Save the video with the boxes drawn on it.
        
    Keep in mind that I want something reusable here ideally.   
"""


@dataclass
class Paths:
    print("Paths for Bohs 6/11/22")
    json_path1: str = r"C:\Users\timf3\PycharmProjects\jetson-camera-code\data\6_11_22\1922-06_11_2022.json"
    json_path2: str = r"C:\Users\timf3\PycharmProjects\jetson-camera-code\data\6_11_22\1945-06_11_2022.json"

    # Note: the spaces here may be an issue.
    video_path1: str = r"C:\Users\timf3\OneDrive - Trinity College Dublin\Documents\Documents\datasets\Datasets\Bohs\6_11_22\time_19_00_09_date_06_11_2022_.avi"
    video_path2: str = r"C:\Users\timf3\OneDrive - Trinity College Dublin\Documents\Documents\datasets\Datasets\Bohs\6_11_22\time_19_00_09_date_06_11_2022_.avi"


class VisualizeDetections:
    def __init__(self, video_path: str, json_path: str, output_path: str):
        self.video_path: str = video_path
        self.json_path: str = json_path
        self.output_path: str = output_path
        self.ball_label: int = 1

        # I might want to see if I can do a sort post init here to initialize these other things.
        self.video_sequence: cv2.VideoCapture = cv2.VideoCapture(self.video_path)
        self.fps = self.video_sequence.get(cv2.CAP_PROP_FPS)
        self.width = int(self.video_sequence.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.video_sequence.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def draw_bboxes(self, image, detections):
        font = cv2.FONT_HERSHEY_SIMPLEX
        for box, label, score  in zip(detections['boxes'], detections['labels'], detections['scores']):
            if label == self.ball_label:
                x1, y1, x2, y2 = box
                x = (x1 + x2) / 2
                y = (y1 + y2) / 2
                color = (0, 0, 255)
                radius = 25
                cv2.circle(image, (int(x), int(y)), radius, color, 2)

                # Round `score` to 2 decimal places, and convert to string
                # score = str(round(score, 2))
                # Getting weird error - will just ignore for now.
                # cv2.putText(image, f"{score}", (max(0, int(x - radius)), max(0, (y - radius - 10))), font,
                #             1,
                #             color, 2)

        return image

    def json_file_iterator(self) -> Iterator[Dict]:
        """
            Returns an iterator of the json file.
            Yielding individual detections

            For example:
                {'boxes': [], 'labels': [], 'scores': [], 'bohs_fps': 4.572921967528001, 'writing_fps': 8.064095365373616, 'reading_fps': 960.8012315022345}
                {'boxes': [[499.5, 447.5, 519.5, 467.5]], 'labels': [1], 'scores': [0.993833065032959], 'bohs_fps': 4.742011144482181, 'writing_fps': 8.169459356867176, 'reading_fps': 969.534323529826}
        """
        with open(self.json_path, 'r') as f:
            yield from json.load(f)['data']

    def visualize_dets(self) -> None:
        """
        Processes the json file, drawing detections onto a video which is saved to the output path.
        """
        # Check if self.video_sequence is open
        if not self.video_sequence.isOpened():
            raise IOError("Couldn't open video")

        print(f"Processing video: {self.video_path} and json: {self.json_path}")

        # Get our generator
        dets = self.json_file_iterator()

        # Create the output video
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        output_sequence = cv2.VideoWriter(filename=self.output_path, fourcc=fourcc, fps=self.fps, frameSize=(self.width, self.height))

        while self.video_sequence.isOpened():
            # Read in the frame
            ret, frame = self.video_sequence.read()

            if not ret:
                print("End of video")
                break

            # Get the next detection from the generator
            det = next(dets)

            # Draw the detections on the frame
            frame = self.draw_bboxes(frame, det)

            # Write the frame to the output video
            output_sequence.write(frame)

        # Release the video
        self.video_sequence.release()
        output_sequence.release()


def main():
    bohs_paths = Paths()
    # First half
    vd1 = VisualizeDetections(bohs_paths.video_path1, bohs_paths.json_path1, "output1.avi")
    vd1.visualize_dets()

    # Second half
    vd2 = VisualizeDetections(bohs_paths.video_path2, bohs_paths.json_path2, "output2.avi")
    vd2.visualize_dets()


if __name__ == '__main__':
    main()

