from PIL import Image, ImageColor, ImageFont, ImageDraw
import cv2
import numpy

from util.BoundingBoxCollection import BoundingBoxCollection
from util.Box import Box


class Frame:
    def __init__(self, pil_image: Image, cv2_image: numpy.ndarray):
        self.__cv2_img__: numpy.ndarray = cv2_image
        self.__pil_img__: Image = pil_image

    @classmethod
    def new_from_pil(cls, pil_image: Image):
        return cls(pil_image, cls.__cv2_from_pil__(pil_image))

    @classmethod
    def new_from_cv2(cls, cv2_image: numpy.ndarray):
        return cls(cls.__pil_from_cv2__(cv2_image), cv2_image)

    def get_pil_img(self) -> Image:
        return self.__pil_img__

    def get_cv2_img(self) -> numpy.ndarray:
        return self.__cv2_img__

    def draw_bounding_boxes(self, box_collection: BoundingBoxCollection):
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
        """Adds a bounding box to an image."""
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
        return Image.fromarray(cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB))

    @staticmethod
    def __cv2_from_pil__(pil_image: Image) -> numpy.ndarray:
        return cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_RGB2BGR)
