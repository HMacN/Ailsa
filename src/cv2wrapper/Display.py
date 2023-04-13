import cv2
from cv2wrapper.Frame import Frame


class Display:
    """
    A wrapper class for the OpenCV2 ImShow class.  This provides a simple API with which to create a single window.
    """

    def __init__(self, window_name='AILSA System'):
        """
        The constructor for the class.

        @param window_name: A str which will be the title displayed a the top of the window.
        """
        self.__window_name__ = window_name

    def show(self, frame: Frame, window_width=800, window_height=600) -> str:
        """
        Displays a single frame.  Allows for adjusting the display area, and can capture single keystrokes from the
        user.

        @param frame:           A Frame object which is to be displayed.
        @param window_width:    An int which is the display width for this frame in pixels.  Defaults to 800.
        @param window_height:   An int which is the display height for this frame in pixels.  Defaults to 600.
        @return:                A str which contains a character corresponding to which key the user pressed.
        """
        if frame is not None:  # and window_is_open() is True:
            cv2.imshow(self.__window_name__, cv2.resize(frame.get_cv2_img(), (window_width, window_height)))
            return cv2.waitKey(10)

    def window_is_open(self) -> bool:
        """
        Checks to see if the window is still open, and returns a boolean with the result.

        @return:    A bool which describes whether or not the window is still open.
        """
        try:
            is_open = cv2.getWindowProperty(self.__window_name__, 0) > -1
            return is_open
        except cv2.error:
            return False

    def hide(self):
        """
        A function to allow the user to stop the window from displaying when it is no longer needed.  For some reason
        this doesn't work, and the window stays open until the program ends.  A few other people online seem to be
        having similar difficulties, and I was not able to find a solution that worked for me.

        @return:
        """
        cv2.destroyWindow(self.__window_name__)
        cv2.destroyAllWindows()
        cv2.waitKey(1)
