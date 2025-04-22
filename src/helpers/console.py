from datetime import datetime

from src.utils.colors import Bgcolor

class Console:

    """
    The Console class provides a lightweight and extensible logging utility for managing output in the terminal with structured formatting, colors, and real-time timestamps. 
    It's designed to enhance the developer and user experience by improving readability, debugging, and log categorization during runtime.

    Purpose:

        * This class handles all console-related operations for:

            - Structured logging with colored labels (INFO, ERROR, DEBUG, etc.)
            - Debug control, allowing conditional logging based on a debug flag
            - Human-readable messages with timestamps
            - Graceful error handling for incorrect log usage

    Key Features:

        1. debugging(self, debug, msg)

            * Conditionally logs a debug message only if the debug flag is True.
            * Uses log_print() to format and display the message in a consistent "DEBUG" style.
            * Helps developers toggle verbose logs without modifying other parts of the code.

        2. log_print(self, status, msg)

            * Main method to output a log message with timestamp and status level.
            * Calls out_log_format() to structure the message before printing.

        3. out_log_format(self, status, msg)

            * Formats log messages with timestamps, colors, and labeled tags (INFO, ERROR, DEBUG, WARNING).
            * Accepts a status string to determine the log level.
            * Each status type is styled using ANSI escape codes (through Bgcolor) for color coding.
            * Falls back to an error message if an unknown status is passed, and terminates the program.

        4. text_format(self, status, msg)

            * Similar to out_log_format(), but without timestamps.
            * Intended for simpler, inline use when a timestamp isn't required.
            * Returns a stylized message string, ideal for banners, summaries, or compact logs.

    Error Handling:

        * Both out_log_format and text_format include checks to ensure only supported status values are used. If not, they:

            - Log an error message.
            - Exit the program with status code 1.

    """

    def debugging(self, debug, msg):
        if debug == True:
            self.log_print("debug", msg=f"{Bgcolor.GRAY}{msg}{Bgcolor.DEFAULT}")

    def log_print(self, status, msg):
        print(self.out_log_format(status, msg))

    def out_log_format(self, status, msg):
        log_time = str(datetime.now().strftime('%Y/%m/%d %H:%M:%S'))

        if status.lower() == "info":
            detailed_info = f"[{Bgcolor.CYAN}{log_time}{Bgcolor.DEFAULT}] [{Bgcolor.BLUE}INFO{Bgcolor.DEFAULT}] {msg}"
            return detailed_info

        if status.lower() == "error":
            detailed_error = f"[{Bgcolor.CYAN}{log_time}{Bgcolor.DEFAULT}] [{Bgcolor.RED}EROR{Bgcolor.DEFAULT}] {msg}"
            return detailed_error

        if status.lower() == "debug":
            detailed_debug = f"[{Bgcolor.CYAN}{log_time}{Bgcolor.DEFAULT}] [{Bgcolor.PURPLE}DBUG{Bgcolor.DEFAULT}] {msg}"
            return detailed_debug

        if status.lower() == "warning":
            detailed_warning = f"[{Bgcolor.CYAN}{log_time}{Bgcolor.DEFAULT}] [{Bgcolor.WARNING}WARN{Bgcolor.DEFAULT}] {msg}"
            return detailed_warning

        if status.lower() not in ["info", "debug", "error", "warning"]:
            self.log_print(status="error", msg="status=REQUIRED args required with msg:{}".format(msg))
            exit(1)

    def text_format(self, status, msg):
        if status.lower() == "info":
            detailed_info = f"[{Bgcolor.BLUE}INFO{Bgcolor.DEFAULT}] {msg}"
            return detailed_info

        if status.lower() == "error":
            detailed_error = f"[{Bgcolor.RED}EROR{Bgcolor.DEFAULT}] {msg}"
            return detailed_error

        if status.lower() == "debug":
            detailed_debug = f"[{Bgcolor.PURPLE}DBUG{Bgcolor.DEFAULT}] {msg}"
            return detailed_debug

        if status.lower() == "warning":
            detailed_warning = f"[{Bgcolor.WARNING}WARN{Bgcolor.DEFAULT}] {msg}"
            return detailed_warning

        if status.lower() not in ["info", "debug", "error", "warning"]:
            self.log_print(status="error", msg="status=REQUIRED args required with msg:{}".format(msg))
            exit(1)