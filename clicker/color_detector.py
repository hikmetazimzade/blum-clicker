import numpy as np
import mss
import cv2
from clicker.logger import get_logger

logger = get_logger()


class Detection:
    """
    A class for detecting objects of specific colors within a defined region of the screen.

    The detection system looks for objects of specific colors (pink, green, and bomb-like colors)
    within the given screen region and ensures that objects near bombs are not considered for actions.

    Attributes:
        start_x (int): X-coordinate of the top-left corner of the screen region.
        start_y (int): Y-coordinate of the top-left corner of the screen region.
        height (int): Height of the screen region.
        width (int): Width of the screen region.
        lower_pink, upper_pink (numpy array): HSV ranges for detecting pink objects.
        lower_green, upper_green (numpy array): HSV ranges for detecting green objects.
        lower_bomb, upper_bomb (numpy array): HSV ranges for detecting bomb-like objects.
    """


    def __init__(self, start_x: int, start_y: int, height: int, width: int):
        """
        Initializes the Detection object with the screen region and color boundaries.

        Args:
            start_x (int): X-coordinate of the top-left corner of the screen region.
            start_y (int): Y-coordinate of the top-left corner of the screen region.
            height (int): Height of the screen region.
            width (int): Width of the screen region.
        """
        self.start_x, self.start_y = start_x, start_y
        self.height, self.width = height, width

        self.lower_pink, self.upper_pink = np.array([160, 20, 100]), np.array([180, 255, 255])
        self.lower_green, self.upper_green = np.array([40, 50, 50]), np.array([80, 255, 255])
        self.lower_bomb, self.upper_bomb = np.array([0, 0, 50]), np.array([180, 50, 200])


    def set_masks(self, frame: cv2.cvtColor) -> None:
        """
        Converts the frame to the HSV color space and sets color masks for detection.

        Args:
            frame (cv2.cvtColor): The frame in which objects need to be detected.
        """
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        self.mask_pink = cv2.inRange(hsv, self.lower_pink, self.upper_pink)
        self.mask_green = cv2.inRange(hsv, self.lower_green, self.upper_green)
        self.mask_bomb = cv2.inRange(hsv, self.lower_bomb, self.upper_bomb)
        self.modify_masks()


    def modify_masks(self):
        """
        Applies morphological operations (erosion and dilation) to clean up the color masks.
        This helps in removing noise and improving the accuracy of object detection.
        """
        mask_pink = cv2.erode(self.mask_pink, None, iterations=1)
        self.mask_pink = cv2.dilate(mask_pink, None, iterations=1)

        mask_green = cv2.erode(self.mask_green, None, iterations=1)
        self.mask_green = cv2.dilate(mask_green, None, iterations=1)

        mask_bomb = cv2.erode(self.mask_bomb, None, iterations=1)
        self.mask_bomb = cv2.dilate(mask_bomb, None, iterations=1)


    def is_bomb_near(self, x: int, y: int, w: int, h: int) -> bool:
        """
        Checks if a detected object is near a bomb-like object.

        Args:
            x (int): X-coordinate of the detected object.
            y (int): Y-coordinate of the detected object.
            w (int): Width of the detected object.
            h (int): Height of the detected object.

        Returns:
            bool: True if a bomb is near the object, False otherwise.
        """
        bomb_contours, _ = cv2.findContours(self.mask_bomb, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        object_center = np.array([x + w // 2, y + h // 2])

        for bomb_cnt in bomb_contours:
            bomb_x, bomb_y, bomb_w, bomb_h = cv2.boundingRect(bomb_cnt)
            bomb_center = np.array([bomb_x + bomb_w // 2, bomb_y + bomb_h // 2])
            distance = np.linalg.norm(bomb_center - object_center)
            if distance < 100:  # If bomb is close enough
                return True
        return False


    def detect_objects(self, mask: cv2.dilate, color_name: str) -> list:
        """
        Detects objects of a specific color in the frame and returns their positions.

        This method identifies the objects in the frame based on the color mask and returns
        their positions unless a bomb is nearby or specific criteria for color are met.

        Args:
            mask (cv2.dilate): The mask for the specific color.
            color_name (str): The name of the color to detect (e.g., "pink", "green").

        Returns:
            list: A list of tuples containing the (x, y) coordinates of detected objects.
        """
        detected_positions = []
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if not self.is_bomb_near(x, y, w, h):
                center_x = x + w // 2
                center_y = y + h // 2
                screen_x = center_x + self.start_x
                screen_y = center_y + self.start_y + 3

                ten_percent_height = int(self.height * 0.1)
                top_limit = self.start_y + ten_percent_height
                bottom_limit = self.start_y + self.height - ten_percent_height

                if color_name == "green" and (center_y < top_limit or center_y > bottom_limit):
                    continue

                detected_positions.append((screen_x, screen_y))

        return detected_positions


    def detect_colors(self, frame: cv2.cvtColor) -> tuple:
        """
        Detects objects of specific colors (pink, green) within the given frame.

        Sets color masks for the frame and detects objects based on those colors. The first pink object,
        if detected, takes priority over green objects.

        Args:
            frame (cv2.cvtColor): The frame in which colors are to be detected.

        Returns:
            tuple: A tuple containing the original frame and the detected positions.
        """
        self.set_masks(frame)
        pink_positions = self.detect_objects(self.mask_pink, "pink")

        if pink_positions:
            return frame, pink_positions[0]

        green_positions = self.detect_objects(self.mask_green, "green")

        return frame,  green_positions


class Capture:
    """
    A utility class for capturing a specific region of the screen using the mss library.
    """

    @staticmethod
    def capture_screen_region(start_x: int, start_y: int, height: int, width: int) -> cv2.cvtColor:
        """
        Captures a screenshot of the specified region of the screen.

        The method uses `mss` to capture the screen, then converts the screenshot
        to a format suitable for processing with OpenCV.

        Args:
            start_x (int): The X-coordinate of the top-left corner of the capture region.
            start_y (int): The Y-coordinate of the top-left corner of the capture region.
            height (int): The height of the capture region.
            width (int): The width of the capture region.

        Returns:
            cv2.cvtColor: The captured frame in BGR color space.
        """
        with mss.mss() as sct:
            region = {
                "top": start_y,
                "left": start_x,
                "width": width,
                "height": height,
            }

            screenshot = sct.grab(region)
            frame = np.array(screenshot)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            return frame