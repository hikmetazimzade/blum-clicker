from decouple import Config, RepositoryEnv
from clicker.logger import get_logger
from typing import Optional
import os


class Coordinate:
    """
    A class to manage the loading and validation of window coordinates from a configuration file.

    The coordinates are read from a text file (`window_coordinates.txt`) using the `decouple` library,
    and the class ensures that they are valid numeric values. If the file or values are invalid,
    warnings are logged, and the process stops.

    Methods:
        get_coordinates(coordinate_path: str) -> Optional[tuple]: Reads and returns valid window coordinates.
        check_coordinates() -> bool: Validates whether the loaded coordinates are numeric.
        check_directory(directory_path: str) -> bool: Checks if the file with coordinates exists in the specified path.
    """


    def get_coordinates(self, coordinate_path: str = "window_coordinates.txt") -> Optional[tuple]:
        """
        Reads and validates the window coordinates from the specified configuration file.

        The method reads the coordinates (`start_x`, `end_x`, `start_y`, `end_y`) from the
        file using the `Config` object from `decouple`. It checks whether the coordinates file
        exists and whether all the coordinates are valid numbers. If successful, it returns the
        coordinates as a tuple.

        Args:
            coordinate_path (str): The path to the file that contains the window coordinates.
                                   Defaults to "window_coordinates.txt".

        Returns:
            Optional[tuple]: A tuple containing (start_x, start_y, width, height) if valid,
                             or `None` if the file or values are invalid.
        """
        self.logger = get_logger()
        if self.check_directory(coordinate_path) == False:
            return

        config = Config(repository=RepositoryEnv(coordinate_path))
        self.start_x, self.end_x = config("start_x"), config("end_x")
        self.start_y, self.end_y = config("start_y"), config("end_y")

        if self.check_coordinates() == False:
            return

        (self.start_x, self.end_x,
         self.start_y, self.end_y) = (int(self.start_x),
                                      int(self.end_x), int(self.start_y), int(self.end_y))

        width, height = self.end_x - self.start_x, self.end_y - self.start_y
        return self.start_x, self.start_y, width, height


    def check_coordinates(self) -> bool:
        """
        Validates whether the coordinates read from the configuration file are numeric.

        This method checks if the `start_x`, `end_x`, `start_y`, and `end_y` values are
        valid digits. If any of the coordinates are not numeric, a warning is logged.

        Returns:
            bool: `True` if all coordinates are numeric, `False` otherwise.
        """
        if not self.start_x.isdigit() or not self.end_x.isdigit() \
                or not self.start_y.isdigit() or not self.end_y.isdigit():
            self.logger.warning("Make sure all coordinates are numbers!")
            return False
        return True


    def check_directory(self, directory_path: str) -> bool:
        """
        Checks whether the specified directory contains the coordinates file.

        The method verifies if the file `window_coordinates.txt` (or any custom file path)
        exists in the provided directory path. If the file is missing, a warning is logged.

        Args:
            directory_path (str): The path to the directory or file to check.

        Returns:
            bool: `True` if the file exists, `False` otherwise.
        """
        abs_path = os.path.abspath(directory_path)

        if not os.path.exists(abs_path):
            self.logger.warning("Make sure window_coordinates.txt file exists in the directory!")
            return False
        return True