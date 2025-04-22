import json
import requests

from src.services.requester import Requester

"""
The release_version() function is a simple yet effective mechanism for retrieving the latest release version of a tool from GitHub. 
It ensures that users are informed about the availability of newer versions and provides a fallback in case the release information cannot be fetched. 
This function is crucial for maintaining the tool up to date, offering smooth integration with GitHub's release system and preventing potential downtime or errors caused by outdated versions.

Key Elements:

    1. CURRENT_VERSION:

        * This constant represents the current, locally installed version of the software tool.
        * This version is used as a fallback in the event that the latest release cannot be fetched from the GitHub repository.

    2. release_version() Function:

        * This function checks the latest release version of the "godork" tool from its official GitHub repository.
        * It performs the following steps:

            - Creating a Session: A session is created using the requests.session() to enable persistent connections, allowing efficient HTTP requests.
            - Making a GET Request: The function sends a GET request to GitHub's API endpoint that provides details about the latest release (https://api.github.com/repos/thd3r/godork/releases/latest).

        * Handling the Response:

            - If the request is successful, the response is expected to be in JSON format. The json.loads() function is used to parse the response body.
            - The parsed data contains various details about the latest release, including the tag name (which represents the version) and the release notes (body). These are returned from the function.

        * Error Handling:

            - If the request fails for any reason (e.g., network issues, API issues), 
              the function catches the exception and returns the current local version (CURRENT_VERSION) along with None for the release notes.

Key Points:

        * GitHub API Integration: The function leverages GitHub's API to fetch the latest release information for the "godork" tool, ensuring that users can easily stay up to date with the latest version.
        * Fallback Mechanism: If there are any issues fetching the release version, the current local version is returned to avoid errors in the application.
        * Error Handling: The use of a try-except block ensures that even if the request to the GitHub API fails, the program will continue running without crashing, and the user will receive information about the current version of the software.

Usage Scenario:

    This function is typically used as part of a larger update management system, where it can be called to check whether a new release is available for the software. 
    If a newer version is found, it can trigger an update process, or if no update is found, the system can reassure the user that they are already using the latest version.

"""

CURRENT_VERSION = "v2.5.4"

def release_version():
    session = requests.session()
    try:
        response = Requester().reqwest(session, "GET", url="https://api.github.com/repos/thd3r/godork/releases/latest", timeout=10)
        data_json = json.loads(response.text)
        return data_json["tag_name"], data_json["body"]
    except:
        return CURRENT_VERSION, None