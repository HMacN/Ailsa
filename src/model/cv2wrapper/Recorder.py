import cv2
from PIL import Image


class Recorder:
    def __init__(self, file_path: str, file_name: str, width=800, height=600):
        self.name = file_name
        self.path = file_path

        four_cc = cv2.VideoWriter_fourcc(*"mp4v")
        # four_cc = -1

        self.video_writer = cv2.VideoWriter(self.name, four_cc, 10, (width, height))

    def set_file_name(self, name: str):
        self.name = name + ".mp4"

    def set_file_path(self, path: str):
        self.path = path

    def add_frame(self, frame: Image):
        self.video_writer.write(frame)
