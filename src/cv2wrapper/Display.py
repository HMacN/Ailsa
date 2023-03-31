import cv2

from cv2wrapper.Frame import Frame
from util.Debugging import debug_print


class Display:
    @staticmethod
    def show(frame: Frame, window_name='AILSA System', window_width=800,
             window_height=600):
        if frame is not None:  # and window_is_open() is True:
            cv2.imshow(window_name, cv2.resize(frame.get_cv2_img(), (window_width, window_height)))
            cv2.waitKey(10)

    @staticmethod
    def window_is_open(window_name='AILSA System') -> bool:
        try:
            is_open = cv2.getWindowProperty(window_name, 0) > -1
            return is_open
        except cv2.error:
            return False

    @staticmethod
    def hide():
        cv2.destroyAllWindows()
