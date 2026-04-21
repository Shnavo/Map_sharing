import datetime as dt
import os

from authentication import get_credentials
from credentials.path import MAP_PATH, DRIVE_ID
from googleapiclient.discovery import build

from typing import TypedDict, TYPE_CHECKING

if TYPE_CHECKING:
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


def list_files_drive(service) -> list[Metadata]:
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
            q=f"'{DRIVE_ID}' in parents",
            pageSize=10,
            fields="nextPageToken, files(id, name, modifiedTime)",
        )
        .execute()
    )

    return file_list.get("files", [])


def date_check(file_list: list[Metadata]) -> str:
    """
    Compares modification timestamps between Google Drive and local files.

    Calculates the time difference to determine which version is newer,
    applying a 20-second tolerance margin to account for server-side
    latency and file system precision drift.

    Args:
        file_list: A list of metadata dictionaries.

    Returns:
        str: Outcome of the comparison:
            - "download": Cloud version is significantly newer.
            - "upload": Local version is significantly newer.
            - "equal": Timestamps are within the tolerance margin.
            - "missing": The provided file_list is empty.

    Note:
        This function relies on the global MAP_PATH constant to locate local files.
    """
    if not file_list:
        return "missing"

    file = file_list[0]
    google = dt.datetime.fromisoformat(file["modifiedTime"])
    drive = dt.datetime.fromtimestamp(
        os.path.getmtime(f"{MAP_PATH}\\{file["name"]}"), dt.timezone.utc
    )

    diff = (google - drive).total_seconds()

    if diff > 20:
        return "download"
    elif diff < -20:
        return "upload"
    else:
        return "equal"
