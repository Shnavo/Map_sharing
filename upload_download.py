from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from googleapiclient.errors import HttpError
from file_check import Metadata
import os


def download_files(service, file_list: list[Metadata], path: str) -> None:
    """
    Downloads file contents from Google Drive and overwrites corresponding local files

    Iterates through the provided file list, fetches binary content using chunks
    via MediaIoBaseDownload, and saves it to the specified local directory.
    Files are opened in write-binary ('wb') mode.

    Args:
        service: Authorized Google Drive API service instance.
        file_list: A list of metadata dictionaries.
        path: Path to local folder containing downloaded files

    Returns:
        None:

    Raises:
        HttpError: If the Google Drive API request fails.
        OSError: If there are issues writing to the local file system (e.g., folder permissions).
    """
    try:
        for item in file_list:
            request = service.files().get_media(fileId=item["id"])
            file = open(os.path.join(path, item["name"]), "wb")
            downloader = MediaIoBaseDownload(file, request)

            done = False
            while done is False:
                done = downloader.next_chunk()[1]

            file.close()

    except HttpError as error:
        print(f"An error occurred during download: {error}")


def upload_files(service, file_list: list[Metadata], path: str) -> None:
    """
    Uploads local files to Google Drive, overwriting them.

    The function matches local files by name based on the provided metadata list.

    Args:
        service: Authorized Google Drive API service instance.
        file_list: A list of metadata dictionaries.
        path: Path to local folder containing files to be uploaded

    Returns:
        None:

    Raises:
        HttpError: If the Google Drive API request fails.
        OSError: If there are issues accessing or reading the local files.
    """
    try:
        for item in file_list:
            media = MediaFileUpload(
                os.path.join(path, item["name"]),
                resumable=True,
            )
            service.files().update(fileId=f"{item["id"]}", media_body=media).execute()

    except HttpError as error:
        print(f"An error occurred during upload: {error}")
