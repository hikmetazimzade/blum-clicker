from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QWidget


class OverlayWidget(QWidget):
    """
    A transparent overlay widget that displays a red rectangular border on the screen.

    The widget is frameless, stays on top of all other windows, and is used to highlight
    a specific area of the screen. The area is defined by the starting coordinates (start_x, start_y)
    and the size (width, height). The red border is drawn using the `paintEvent` method.

    Args:
        start_x (int): The X-coordinate of the top-left corner of the overlay.
        start_y (int): The Y-coordinate of the top-left corner of the overlay.
        width (int): The width of the overlay.
        height (int): The height of the overlay.
    """


    def __init__(self, start_x: int, start_y: int, width: int, height: int):
        """
        Initializes the overlay widget with the specified geometry and appearance.

        The widget is frameless, always stays on top of other windows, and has a translucent
        background to make it blend into the screen. The overlay is defined by its
        starting coordinates and dimensions.

        Args:
            start_x (int): The X-coordinate of the top-left corner of the overlay.
            start_y (int): The Y-coordinate of the top-left corner of the overlay.
            width (int): The width of the overlay area.
            height (int): The height of the overlay area.
        """
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setGeometry(start_x, start_y, width, height)


    def paintEvent(self, event):
        """
        Handles the paint event to draw the red rectangular border.

        This method is automatically called when the widget needs to be repainted.
        It draws a red border around the edges of the overlay widget to highlight
        the defined area on the screen.

        Args:
            event (QPaintEvent): The event object that contains information about
                                 the painting event.
        """
        painter = QPainter(self)
        pen = QPen(Qt.red, 5)

        painter.setPen(pen)
        painter.drawRect(QRect(0, 0, self.width(), self.height()))