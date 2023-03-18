import cv2
import numpy as np

from util.DebugPrint import debug_print


def show(frame=np.zeros((350, 700, 3), dtype=np.uint8), window_name='AILSA System', window_width=800,
         window_height=600):
    if frame is not None:  # and window_is_open() is True:
        cv2.imshow(window_name, cv2.resize(frame, (window_width, window_height)))
        cv2.waitKey(10)


def window_is_open(window_name='AILSA System') -> bool:
    try:
        is_open = cv2.getWindowProperty(window_name, 0) > -1
        return is_open
    except cv2.error:
        return False


def hide():
    cv2.destroyAllWindows()


class Display:
    ...
