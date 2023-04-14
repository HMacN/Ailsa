from PIL import Image, ImageColor, ImageFont, ImageDraw
import cv2
import numpy

from util.BoxList import BoxList
from util.Box import Box


class Frame:
    """
    A wrapper class to hold all image recording and encoding.  So far this project uses two image formats, PIL and
    numpy.ndarray.  This class should allow for easy use of whichever image format is required.

    Note that to improve performance, both forms of image are generated on class instantiation, and then passed to the
    user as required, rather than doing multiple conversions between image formats.
    """
    def __init__(self, pil_image: Image, cv2_image: numpy.ndarray):
        """
        The 'true' constructor for this class.  As it requires the same image in both formats, it is envisioned that
        this function is not called by the user, and instead the two 'new_from_...' functions should be used to
        instantiate this class from a single image in whichever format is available.

        @param pil_image: A PIL.Image object which is the image to store.
        @param cv2_image: A numpy.ndarray which is the image to store.
        """
        self.__cv2_img__: numpy.ndarray = cv2_image
        self.__pil_img__: Image = pil_image

    @classmethod
    def new_from_pil(cls, pil_image: Image):
        """
        A constructor function which generates an instance of this class from a PIL.Image object.

        @param pil_image: A PIL.Image object to create a Frame object from.
        @return:
        """
        return cls(pil_image, cls.__cv2_from_pil__(pil_image))

    @classmethod
    def new_from_cv2(cls, cv2_image: numpy.ndarray):
        """
        A constructor function which generates an instance of this class from a numpy.ndarray object.

        @param cv2_image: A numpy.ndarray object (the CV2 image format) to create a Frame object from.
        @return:
        """
        return cls(cls.__pil_from_cv2__(cv2_image), cv2_image)

    def get_pil_img(self) -> Image:
        """
        A getter for the PIL.Image form of the image in this frame.

        @return: A PIL.Image object which is the picture in this Frame.
        """
        return self.__pil_img__

    def get_cv2_img(self) -> numpy.ndarray:
        """
        A getter for the numpy.ndarray object (the CV2 image format) form of the image in this frame.

        @return: A numpy.ndarray object (the CV2 image format) which is the picture in this Frame.
        """
        return self.__cv2_img__

    def draw_bounding_boxes(self, box_collection: BoxList):
        """
        Draw the given set of bounding boxes onto the picture in this frame.

        @param box_collection:  A BoxList object which contains the boxes to draw onto the Frame.
        @return:
        """
        colors = list(ImageColor.colormap.values())
        font = ImageFont.load_default()
        pil_img = self.__pil_img__

        for i in range(box_collection.size()):
            box: Box = box_collection.get(i)
            display_str = box.label + ": " + str(round(box.confidence * 100, 1)) + "%"
            color = colors[hash(box.label) % len(colors)]

            self.__draw_bounding_box_on_image__(y_min=box.lower_edge, x_min=box.left_edge, y_max=box.upper_edge,
                                                x_max=box.right_edge, color=color, font=font,
                                                display_str_list=[display_str])

        self.__pil_img__ = pil_img
        self.__cv2_img__ = self.__cv2_from_pil__(pil_img)

    def __draw_bounding_box_on_image__(self,
                                       y_min,
                                       x_min,
                                       y_max,
                                       x_max,
                                       color,
                                       font,
                                       thickness=4,
                                       display_str_list=()):
        """
        The function to actually draw a single bounding box onto the image.  Note that this can only happen in PIL
        format, so the cv2 format image will need drawn on elsewhere.

        @param y_min:               The minimum y coordinate of the box.
        @param x_min:               The minimum x coordinate of the box.
        @param y_max:               The maximum y coordinate of the box.
        @param x_max:               The maximum x coordinate of the box.
        @param color:               The colour of the box.
        @param font:                The font to be used for the label of the box.
        @param thickness:           The thickness of the lines the box is to be drawn with.
        @param display_str_list:    A list of str values to print to the label of the box.
        @return:
        """
        draw = ImageDraw.Draw(self.__pil_img__)
        im_width, im_height = self.__pil_img__.size
        (left, right, top, bottom) = (x_min * im_width, x_max * im_width,
                                      y_min * im_height, y_max * im_height)
        draw.line([(left, top), (left, bottom), (right, bottom), (right, top),
                   (left, top)],
                  width=thickness,
                  fill=color)

        # If the total height of the display strings added to the top of the bounding
        # box exceeds the top of the image, stack the strings below the bounding box
        # instead of above.
        display_str_heights = [font.getbbox(ds)[1] for ds in display_str_list]
        # Each display_str has a top and bottom margin of 0.05x.
        total_display_str_height = (1 + 2 * 0.05) * sum(display_str_heights)

        if top > total_display_str_height:
            text_bottom = top
        else:
            text_bottom = top + total_display_str_height
        # Reverse list and print from bottom to top.
        for display_str in display_str_list[::-1]:
            box = font.getbbox(display_str)
            text_width = box[2]
            text_height = box[3]
            margin = numpy.ceil(0.05 * text_height)
            t1: float = left
            t2: float = text_bottom - text_height - 2 * margin
            t3: float = left + text_width
            t4: float = text_bottom
            draw.rectangle((t1, t2, t3, t4),
                           fill=color)
            draw.text((left + margin, text_bottom - text_height - margin),
                      display_str,
                      fill="black",
                      font=font)
            text_bottom -= text_height - 2 * margin

    @staticmethod
    def __pil_from_cv2__(cv2_image: numpy.ndarray) -> Image:
        """
        A function to convert a numpy.ndarray (cv2 image format) to a PIL.

        @param cv2_image:   The numpy.ndarray object that is to be converted to a PIL.
        @return:            A PIL.Image object which was created from the numpy.ndarray.
        """
        return Image.fromarray(cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB))

    @staticmethod
    def __cv2_from_pil__(pil_image: Image) -> numpy.ndarray:
        """
        A function to convert a PIL to a numpy.ndarray (cv2 image format).

        @param pil_image:   The PIL.Image object that is to be converted to a numpy.ndarray.
        @return:            A numpy.ndarray object which was created from the PIL.
        """
        return cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_RGB2BGR)
