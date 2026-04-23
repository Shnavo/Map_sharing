import datetime as dt
import os
from authentication import get_credentials
from googleapiclient.discovery import build
from typing import TypedDict, TYPE_CHECKING
from googleapiclient.discovery import Resource


class Metadata(TypedDict):
    id: str
    name: str
    modifiedTime: str


def create_service() -> Resource:
    """
    Initializes and returns a Google Drive API service object.

    This function leverages the retrieved credentials to establish a connection
    with the Google Drive V3 API. The resulting Resource object serves as the
    primary entry point for all API interactions (listing, uploading, and downloading).

    Returns:
        Resource: A pre-configured Google Drive API service instance
            ready to execute requests.

    Raises:
        googleapiclient.errors.UnknownApiNameOrVersion: If "drive" or "v3"
            parameters are incorrect.
    """
    creds = get_credentials()
    return build("drive", "v3", credentials=creds)


def list_files_drive(service, drive_id) -> list[Metadata]:
    """
    Fetches a list of files from a specific Google Drive folder.

    Args:
        service: Authorized Google Drive API service instance.

    Returns:
        list[Metadata]: A list of dictionaries containing metadata for requested files.
    """
    file_list = (
        service.files()
        .list(
            q=f"'{drive_id}' in parents",
            pageSize=10,
            fields="nextPageToken, files(id, name, modifiedTime)",
        )
        .execute()
    )

    return file_list.get("files", [])


def date_check(file_list: list[Metadata], path) -> str:
    """
    Checks if the file is present and compares modification timestamps between Google Drive and local files.

    If file is present, calculates the time difference to determine which
    version is newer, applying a 20-second tolerance margin to account for
    server-side latency and file system precision drift.

    Args:
        file_list: A list of metadata dictionaries.
        path: The local directory path where the files are stored.

    Returns:
        str: Outcome of the comparison:
            - "download": Cloud version is significantly newer or the file is not present locally.
            - "upload": Local version is significantly newer.
            - "equal": Timestamps are within the tolerance margin.
            - "missing": The provided file_list is empty.
    """
    if not file_list:
        return "missing"

    file = file_list[0]
    if not os.path.isfile(os.path.join(path, file["name"])):
        return "download"

    google = dt.datetime.fromisoformat(file["modifiedTime"])
    drive = dt.datetime.fromtimestamp(
        os.path.getmtime(os.path.join(path, file["name"])), dt.timezone.utc
    )

    diff = (google - drive).total_seconds()

    if diff > 20:
        return "download"
    elif diff < -20:
        return "upload"
    else:
        return "equal"


def setup_creds() -> None:
    """
    Ensures the required directory structure and credential files exist.

    This function checks for the 'credentials' folder and the 'credentials.json'
    file. If the folder is missing, it creates it. If the JSON file is missing,
    it enters a loop, pausing execution and prompting the user to provide
    the file before continuing.

    Note:
        This is a blocking function. It will not allow the program to proceed
        until 'credentials.json' is detected in the correct path.
    """
    if not os.path.isdir(os.path.abspath("credentials")):
        os.mkdir(f"{os.getcwd()}\\credentials")
    check = os.path.isfile(os.path.join(os.path.abspath("credentials"), "credentials.json"))
    while check == False:
        input(
            "Please put the 'credentials.json' inside the folder called "
            "'credentials' in the location of this program and press enter when done"
        )
        if os.path.isfile(os.path.join(os.path.abspath("credentials"), "credentials.json")):
            check = True


def create_paths() -> tuple[str, str]:
    """
    Handles the first-time setup by gathering folder paths from the user.

    Prompts the user for the local synchronization directory and the Google
    Drive folder ID. These values are normalized and saved to 'path.txt'
    for future sessions.

    Returns:
        tuple[str, str]: A tuple containing the absolute local path and the Drive ID.

    Note:
        This function is triggered only when 'path.txt' is not found in the
        'credentials' directory.
    """
    cred_path = os.path.abspath("credentials")
    file_path = os.path.join(cred_path, "path.txt")
    with open(file_path, "w+", encoding="utf-8") as f:
        drive_id = input(
            "Please paste the 'drive id' of the Google Drive location "
            "where the shared files are/need to be located. \n"
            "It is the string of letters and numbers in the URL of the"
            "Google Drive folder after 'folders/':\n"
        ).strip()
        path = (
            input(
                "Please paste the path to the folder where the files "
                "are/need to be located on your hard drive. \n"
                "If you're not sure check on the internet how to reach that location:\n"
            )
            .strip()
            .strip('"')
        )
        path = os.path.abspath(path)
        f.write(f'PATH = "{path}"' "\n" f'DRIVE_ID = "{drive_id}"')
    return path, drive_id


def startup() -> tuple[str, str]:
    """
    Retrieves configuration paths from the local storage or initiates setup.

    The function checks for the existence of 'path.txt'. If found, it parses
    the file and strips formatting to extract the raw local path and Drive ID.
    If the file is missing, it redirects to the 'create_paths' setup flow.

    Returns:
        tuple[str, str]: A tuple containing the absolute local path and the Drive ID.
    """
    cred_path = os.path.abspath("credentials")

    if not os.path.isfile(file := os.path.join(cred_path, "path.txt")):
        return create_paths()

    with open(file, encoding="utf-8") as f:
        lines = f.read().splitlines()

    path, drive_id = lines[0], lines[1]
    path = path.split("=")[1].strip().strip('"')
    drive_id = drive_id.split("=")[1].strip().strip('"')

    return path, drive_id
