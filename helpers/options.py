import argparse

class OptionParser:

    """
    The OptionParser class is a lightweight, static utility that serves as the command-line interface (CLI) parser for the GoDork tool. 
    It leverages Python's built-in argparse module to handle user input from the terminal, making the tool both flexible and easy to configure.

    Purpose:

        * This class is responsible for:

            - Defining all supported command-line options
            - Validating and parsing input from the terminal
            - Returning the parsed arguments for use within the application

    Key Features:

        1. argument_parser() (static method)

            * This is the core method of the class. 
              It creates and configures an ArgumentParser instance with several options to tailor the scraping behavior.
            * The method returns a parsed Namespace object that contains all user-specified or default values. This object is then used throughout the tool to control execution flow and feature toggles.

    """

    @staticmethod
    def argument_parser():
        parser = argparse.ArgumentParser(
            prog="godork",
            usage="%(prog)s [OPTIONS] "
        )
        parser.add_argument(
            "-v",
            "--version",
            action="version",
            version=f"%(prog)s 2.0.5",
        )
        parser.add_argument(
            "-d",
            "--dorks",
            action="store",
            default="",
            help="single dork or file containing multiple dorks"
        )
        parser.add_argument(
            "-p",
            "--proxy",
            action="store",
            help="http proxy to use with godork (e.g. http://127.0.0.1:8080)"
        )
        parser.add_argument(
            "--debug",
            action="store_true",
            default=False,
            help="show detailed logs and error for debugging"
        )
        parser.add_argument(
            "--retries",
            type=int,
            action="store",
            default=40,
            help="retries when request is blocked (default: 40)"
        )
        parser.add_argument(
            "--max-retries",
            type=int,
            action="store",
            default=2,
            help="max attempts to bypass protection mechanisms (default: 2)"
        )
        parser.add_argument(
            "--no-headless",
            action="store_false",
            default=True,
            help="run in graphical mode when bypassing"
        )
        parser.add_argument(
            "--update-tool",
            action="store_true",
            default=False,
            help="update godork to the latest version"
        )

        return parser.parse_args()