import cv2
import numpy as np

from util.DebugPrint import debug_print


def show(frame=np.zeros((350, 700, 3), dtype=np.uint8), window_name='AILSA System', window_width=800,
         window_height=600):

    cv2.imshow(window_name, cv2.resize(frame, (window_width, window_height)))
    cv2.waitKey(100)


def closed_by_user(window_name='AILSA System') -> bool:
    is_closed = cv2.getWindowProperty(window_name, 0) < 0
    return is_closed


def hide():
    cv2.destroyAllWindows()


class Display:
    ...
