from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
import sys
import time
import keyboard
import mouse
from clicker.logger import get_logger
from clicker.window_marker import OverlayWidget
from clicker.coordinate_controller import Coordinate
from clicker.color_detector import Detection, Capture


def initialize_logger():
    """
    Initializes and configures the logger for the Blum AutoClicker Bot.

    Logs essential information about how to use the bot, including the controls
    and author details. This logger will display relevant debug and info messages.

    Returns:
        logger (Logger): A logger instance with the initialized settings.
    """
    logger = get_logger()
    logger.debug("Welcome to Blum AutoClicker Bot!")
    logger.debug("Author: https://github.com/hikmetazimzade\n")
    logger.debug("Before starting, make sure that:")
    logger.debug("Telegram Blum Window Is Inside Red Area\n")

    logger.info("Controls:")
    logger.info("  - Press 's' to start the bot")
    logger.info("  - Press 'p' to stop the bot")
    logger.info("  - Press CTRL + C to exit the program")

    logger.debug("Bot is ready to start. Waiting for user input...")
    return logger


def get_coordinates():
    """
    Retrieves the coordinates for the area to be monitored by the bot.

    It fetches the screen coordinates where the detection will occur using
    the Coordinate class.

    Returns:
        tuple: Coordinates in the format (start_x, start_y, width, height) for
        the area to monitor.

    Exits:
        If no coordinates are found, the function exits the application with an error message.
    """
    coordinates = Coordinate().get_coordinates()
    if coordinates is None:
        time.sleep(3)
        sys.exit()

    return coordinates


def create_overlay(start_x, start_y, width, height):
    """
    Creates an overlay window at the specified coordinates on the screen.

    This function shows a transparent overlay window that marks the area being
    monitored by the bot, ensuring that the user can visually identify it.

    Args:
        start_x (int): The X-coordinate of the starting point.
        start_y (int): The Y-coordinate of the starting point.
        width (int): The width of the area.
        height (int): The height of the area.

    Returns:
        OverlayWidget: An instance of the overlay widget that is displayed.
    """
    overlay = OverlayWidget(start_x, start_y, width, height)
    overlay.show()
    return overlay


def check_keyboard_input(running):
    """
    Checks if specific keys ('s' or 'p') have been pressed to control the bot's state.

    This function listens for keyboard inputs to start ('s') or stop ('p') the bot.
    If 's' is pressed, it sets the bot to running state. If 'p' is pressed, it
    pauses the bot.

    Args:
        running (bool): Current running state of the bot.

    Returns:
        bool: Updated running state based on the key press.
    """
    if keyboard.is_pressed('s'):
        return True

    elif keyboard.is_pressed('p'):
        return False

    elif keyboard.is_pressed("ctrl+c"):
        sys.exit()

    return running


def log_state_transition(logger, running, was_running, was_paused):
    """
    Logs the transition between different states of the bot (running or paused).

    Logs a message indicating whether the bot has started or paused based on
    the current state transitions.

    Args:
        logger (Logger): The logger instance to log messages.
        running (bool): Current running state.
        was_running (bool): Previous running state.
        was_paused (bool): Previous paused state.

    Returns:
        tuple: A tuple (was_running, was_paused) indicating the updated states
        after logging transitions.
    """
    if running and not was_running:
        logger.info("Started Bot...")
        return True, False

    if not running and not was_paused:
        logger.info("Paused Bot...")
        return False, True
    return was_running, was_paused


def perform_detection(start_x, start_y, width, height):
    """
    Performs the color detection and initiates actions (clicks) based on the detected colors.

    Captures the screen in the specified region and processes the captured frame
    to detect specific colors. If detection occurs, it triggers mouse clicks at
    the appropriate positions.

    Args:
        start_x (int): The X-coordinate of the starting point.
        start_y (int): The Y-coordinate of the starting point.
        width (int): The width of the area.
        height (int): The height of the area.
    """
    frame = Capture.capture_screen_region(start_x, start_y, height, width)
    processed_frame, click_positions = Detection(start_x, start_y, height, width).detect_colors(frame)
    if click_positions:
        handle_click_positions(click_positions)


def handle_click_positions(click_positions):
    """
    Handles mouse clicks based on the detected click positions.

    Moves the mouse pointer to the detected click positions and clicks.
    The positions can either be a single tuple or a list of multiple positions.

    Args:
        click_positions (tuple or list): Detected click positions in (x, y) format.
    """
    if isinstance(click_positions, tuple) and len(click_positions) == 2:
        mouse.move(click_positions[0], click_positions[1], absolute=True, duration=0)
        mouse.click()

    elif isinstance(click_positions, list) and len(click_positions) > 0:
        for position in click_positions:
            mouse.move(position[0], position[1], absolute=True, duration=0)
            mouse.click()


def handle_detection(logger, start_x, start_y, width, height):
    """
    Manages the bot's detection logic and its state (running or paused).

    Continuously monitors the state of the bot (running or paused), handles the
    transitions between states, and triggers detection when the bot is running.

    Args:
        logger (Logger): The logger instance for logging state changes.
        start_x (int): The X-coordinate of the starting point.
        start_y (int): The Y-coordinate of the starting point.
        width (int): The width of the area.
        height (int): The height of the area.

    Returns:
        function: A closure function (detection_loop) that performs detection
        in an event loop.
    """
    running = False
    was_running = False
    was_paused = True

    def detection_loop():
        nonlocal running, was_running, was_paused

        running = check_keyboard_input(running)
        was_running, was_paused = log_state_transition(logger, running, was_running, was_paused)

        if running:
            perform_detection(start_x, start_y, width, height)

    return detection_loop


def main() -> None:
    """
    The main entry point of the Blum AutoClicker Bot application.

    Initializes the logger, retrieves the coordinates for the detection area,
    creates the overlay, and starts the bot's detection logic in an event loop.

    Exits:
        The application exits when the event loop ends or if there are no coordinates.
    """
    logger = initialize_logger()
    coordinates = get_coordinates()

    app = QApplication(sys.argv)

    start_x, start_y, width, height = coordinates
    overlay = create_overlay(start_x, start_y, width, height)

    detection_loop = handle_detection(logger, start_x, start_y, width, height)

    timer = QTimer()
    timer.timeout.connect(detection_loop)
    timer.start(10)  # Check every 10 ms

    sys.exit(app.exec_())


if __name__ == "__main__":
    from config import ROOT_DIR
    import os

    os.chdir(ROOT_DIR)
    main()