import os
import json

from datetime import datetime
from src.helpers.console import Console

class Reports:

    """
    The Reports class is a centralized utility designed to manage logging and reporting for the GoDork tool. 
    Its primary role is to handle output storage by writing execution logs and structured JSON results to organized directories, ensuring traceability and easy analysis of scraping sessions.

    Purpose:

        * This class automates the creation, formatting, and saving of:

            - Log files in plain text (human-readable)
            - JSON reports for structured, machine-readable data
            - Organized directories for persistent reporting
    
    Key Features:

        1. Initialization (__init__)

            * Upon initialization:

                - Determines the appropriate temp directory (Windows or Unix-based systems)
                - Sets up paths for logs and JSON reports using timestamps
                - Automatically creates required directories (logs and json) under /tmp/godork/reports (or %TEMP%/godork/reports on Windows)
                - Initializes the Console utility for consistent and colored terminal output

        2. write_file_json(filename, data)

            * Appends structured data to a JSON file. Ideal for storing detailed metadata or search results.

        3. write_file_text(filename, data)

            * Appends plain text to a given file. Primarily used for saving logs and console-style outputs.

        4. logs_report(status, data)

            * Handles writing formatted log entries (with timestamps and status levels like INFO, ERROR, DEBUG) to the log file. Uses the Console class for formatting consistency.

        5. json_report(data)

            * Writes a JSON entry to the report file. Useful for capturing individual result items in structured form.

    Report Paths:

        * Logs: Saved under reports/logs/ with timestamped filenames.
        * JSON: Saved under reports/json/ for structured result data.

    Error Handling:

        * Both logs_report() and json_report() include internal exception handling. If writing to a file fails, an error is printed to the console, ensuring that such failures are visible but non-fatal.

    """

    def __init__(self):
        self.temp_dir = os.getenv("TEMP") if os.name == "nt" else "/tmp"
        self.base_dir = f"{self.temp_dir}/godork/reports"

        self.log_file = f"{self.base_dir}/logs/{str(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))}_godork.log"
        self.json_file = f"{self.base_dir}/json/{str(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))}_godork.json"

        self.console = Console()

        try:
            os.makedirs(f"{self.base_dir}/logs")
            os.makedirs(f"{self.base_dir}/json")
        except FileExistsError:
            self.base_dir = self.base_dir

    def write_file_json(self, filename, data):
        with open(filename, "at") as f:
            try:
                f.write(json.dumps(data, indent=4, ensure_ascii=False) + os.linesep)
            finally:
                f.close()

    def write_file_text(self, filename, data):
        with open(filename, "at") as f:
            try:
                f.write(str(data) + os.linesep)
            finally:
                f.close()

    def logs_report(self, status, data):
        try:
            self.write_file_text(self.log_file, data=self.console.out_log_format(status, msg=data))
        except Exception as err:
            self.console.log_print("error", msg=err)

    def json_report(self, data):
        try:
            self.write_file_json(self.json_file, data=data)
        except Exception as err:
            self.console.log_print("error", msg=err)