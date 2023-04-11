import cv2

from cv2wrapper.Frame import Frame
from util.Debugging import debug_print


class Display:

    def __init__(self, window_name='AILSA System'):
        self.__window_name__ = window_name

    def show(self, frame: Frame, window_width=800, window_height=600) -> str:
        if frame is not None:  # and window_is_open() is True:
            cv2.imshow(self.__window_name__, cv2.resize(frame.get_cv2_img(), (window_width, window_height)))
            return cv2.waitKey(10)

    def window_is_open(self) -> bool:
        try:
            is_open = cv2.getWindowProperty(self.__window_name__, 0) > -1
            return is_open
        except cv2.error:
            return False

    def hide(self):
        cv2.destroyWindow(self.__window_name__)
        cv2.destroyAllWindows()
        cv2.waitKey(1)
