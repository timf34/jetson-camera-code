import cv2

from typing import List, Dict


"""
    Plan:
        - Write function to parse the Json file 
        - Run through the json file (can create an iterator) and video frame by frame, and draw a box if there's a detection. 
        - Save the video with the boxes drawn on it.
"""

class VisualizeDetections:
    def __init__(self, video_path: str, json_path: str, output_path: str):
        self.video_path: str = video_path
        self.json_path: str = json_path
        self.ball_label: int = 1

        # I might want to see if I can do a sort post init here to initialize these other things.
        self.video_sequence: cv2.VideoCapture = cv2.VideoCapture(self.video_path)
        self.fps = self.video_sequence.get(cv2.CAP_PROP_FPS)
        self.width = self.video_sequence.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.video_sequence.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def draw_bboxes(self, image, detections):
        font = cv2.FONT_HERSHEY_SIMPLEX
        for box, label, score in zip(detections['boxes'], detections['labels'], detections['scores']):
            if label == self.ball_label:
                x1, y1, x2, y2 = box
                x = (x1 + x2) / 2
                y = (y1 + y2) / 2
                color = (0, 0, 255)
                radius = 25
                cv2.circle(image, (int(x), int(y)), radius, color, 2)
                cv2.putText(image, '{:0.2f}'.format(score), (max(0, int(x - radius)), max(0, (y - radius - 10))), font,
                            1,
                            color, 2)

        return image

