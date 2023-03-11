import cv2


def show(frame, window_name='AILSA System', window_width=800, window_height=600) -> bool:
    try:
        cv2.imshow(window_name, cv2.resize(frame, (window_width, window_height)))
        cv2.waitKey(100)
        return cv2.getWindowProperty(window_name, 0) >= 0
    except cv2.error:
        return False


def hide():
    cv2.destroyAllWindows()


class Display:
    ...
