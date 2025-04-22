import shutil
import tempfile
import subprocess

from pathlib import Path

from utils.colors import Bgcolor
from utils.banner import print_banner
from helpers.console import Console
from services.version import CURRENT_VERSION, release_version

class UpdateTool:

    """
    The UpdateTool class is a vital component for managing the updates of a software tool, specifically designed to check for new versions of a repository, download the latest release, and update the local installation. 
    This class ensures that the user is always running the most up-to-date version, providing feedback on the status of the update process.

    Key Features:

        1. Initialization (__init__):

            * The class initializes the repository URL (repo_url), which points to the GitHub repository of the tool to be updated (in this case, "godork")
            * The Console instance is also initialized for handling console output, ensuring logs and updates are displayed to the user.

        2. Version Check (check_version):

            * This method checks the current version of the tool against the latest release version available in the repository.
            * It retrieves the release version from the release_version() function and compares it with the current version (CURRENT_VERSION).

                - If the current version is outdated, it displays a banner indicating that an update is needed.
                - If the current version is the latest, it displays a "latest" banner.
                - If the release version is unavailable, it flags the tool as outdated.

        3. Downloading Updates (download_updates):

            * This method handles the process of downloading and updating the tool by cloning the latest version of the repository from GitHub.
            * It accepts several parameters like the base directory (base_dir), release version (release_vers), and update data (body).
            * The update process involves:

                - Creating a temporary directory to clone the latest version from GitHub using git clone.
                - Clearing the current installation by removing all files and directories in the base_dir.
                - Copying the updated files from the cloned repository into the base directory.
                - Finally, it prints a success message, confirming the update from the current version to the new release version, along with any relevant update information.

            * If an error occurs during the update process, it catches and prints the exception with an error message.

        4. Update the Tool (update_tool):

            * This method orchestrates the process of checking for updates and applying them if necessary.
            * It retrieves the latest release version and compares it with the current version:

                - If an update is available, it prints an informational message and proceeds to download and apply the update using the download_updates method.
                - If the current version is already up to date, it informs the user that the tool is already at the latest version.
                - If the latest version cannot be determined, it notifies the user of the failure to fetch the latest release information.
                    
    """

    def __init__(self):
        self.repo_url = "https://github.com/thd3r/godork"
        self.console = Console()

    def check_version(self):
        release_vers, _ = release_version()
        if release_vers is not None and CURRENT_VERSION < release_vers:
            print_banner(status=f"{Bgcolor.RED}outdated{Bgcolor.DEFAULT}")
        if release_vers is not None and CURRENT_VERSION == release_vers:
            print_banner(status=f"{Bgcolor.GREEN}latest{Bgcolor.DEFAULT}")
        if release_vers is None:
            print_banner(status=f"{Bgcolor.RED}outdated{Bgcolor.DEFAULT}")

    def download_updates(self, **kwargs):
        current_dir = kwargs.get('base_dir')
        release_vers = kwargs.get('release_vers')
        data_update = kwargs.get('body')

        try:
            temp_dir = Path(tempfile.mkdtemp(prefix=f"godork-{release_vers}-"))
            subprocess.run(["git", "clone", "--branch", "main", self.repo_url, str(temp_dir)], check=True)
                
            current_dir = kwargs.get('base_dir')

            for item in current_dir.iterdir():
                if item.is_file():
                    item.unlink()
                else:
                    shutil.rmtree(item)

            for item in temp_dir.iterdir():
                target = current_dir / item.name

                if item.is_dir():
                    shutil.copytree(item, target)
                else:
                    shutil.copy2(item, target)

            print(self.console.text_format("info", f"godork sucessfully updated {CURRENT_VERSION} -> {release_vers} ({Bgcolor.GREEN}latest{Bgcolor.DEFAULT})"))
            print(f"{Bgcolor.PURPLE}{data_update}{Bgcolor.DEFAULT}")

        except Exception as err:
            print(self.console.text_format("error", f"Failed to download update... {Bgcolor.BLUE}reason{Bgcolor.DEFAULT}:{err}"))
    
    def update_tool(self, base_dir):
        release_vers, body = release_version()
        
        if release_vers is not None and CURRENT_VERSION < release_vers:
            print(self.console.text_format("info", f"Release version available {release_vers}"))
            print(self.console.text_format("info", f"Updating godork {CURRENT_VERSION} → {release_vers}..."))

            self.download_updates(base_dir=base_dir, release_vers=release_vers, body=body)
        if release_vers is not None and CURRENT_VERSION == release_vers:
            print(self.console.text_format("info", f"godork {CURRENT_VERSION} is up to date"))
        if release_vers is None:
            print(self.console.text_format("info", f"Cant find the latest version of godork"))