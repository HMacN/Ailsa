import cv2
from PIL import Image

from cv2wrapper.Frame import Frame


class Recorder:
    def __init__(self, file_name="new_file", file_path=".\\", width=800, height=600):
        self.name = file_name + ".mp4"
        self.path = file_path

        self.four_cc = cv2.VideoWriter_fourcc(*"mp4v")
        self.video_writer = cv2.VideoWriter(self.name, self.four_cc, 10, (width, height))

    def add_frame(self, frame: Frame):
        self.video_writer.write(frame.get_cv2_img())
