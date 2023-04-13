import cv2

from cv2wrapper.Frame import Frame


class Recorder:
    """
    A wrapper class that holds a cv2.VideoWriter.  This class provides a simple API to allow writing Frame objects to a
    video (.mp4) file.
    """
    def __init__(self, file_name="new_file", file_path=".\\", width=800, height=600):
        """
        The constructor for this class.  Creates the file to write to.

        @param file_name:   A str which is the name of the file to write to.  Defaults to "new file".
        @param file_path:   A str which is the directory to create the file in.  Defaults to ".\\".
        @param width:       An int which is the width (in pixels) of the Frames which will be written to this file.
        @param height:      An int which is the height (in pixels) of the Frames which will be written to this file.
        """
        self.name = file_name + ".mp4"
        self.path = file_path

        self.four_cc = cv2.VideoWriter_fourcc(*"mp4v")
        self.video_writer = cv2.VideoWriter(self.name, self.four_cc, 10, (width, height))

    def add_frame(self, frame: Frame):
        """
        Writes (adds) a single Frame object to the .mp4 file being written.

        @param frame:   The Frame object to add to the file.
        @return:
        """
        self.video_writer.write(frame.get_cv2_img())
