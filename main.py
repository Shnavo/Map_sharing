from file_check import *
from upload_download import download_files, upload_files
import os


def main():
    """
    Orchestrates the map synchronization process between local storage and Google Drive.

    The workflow follows these steps:
    0. Environment Check: Ensures 'credentials.json' exists and loads paths from 'path.txt'.
    1. Authentication: Initializes the Google Drive API service instance.
    2. Metadata Fetch: Retrieves file information from the specified Google Drive folder.
    3. Conflict Resolution: Compares cloud and local timestamps with a 20-second tolerance.
    4. Action Execution:
        - Downloads cloud versions if they are newer or missing locally.
        - Uploads local versions if they are newer than the cloud versions.
        - Raises an exception if the remote folder is empty.
        - Finishes if files are already in sync.

    Execution flow is managed via 'date_check' logic to optimize bandwidth usage.
    """
    if not os.path.isfile(os.path.join("credentials", "credentials.json")):
        setup_creds()
    path, drive_id = startup()
    service = create_service()
    file_list = list_files_drive(service, drive_id)
    action = date_check(file_list, path)
    if action == "download":
        download_files(service, file_list, path)
        return
    if action == "upload":
        upload_files(service, file_list, path)
        return
    if action == "missing":
        print("Error: The Google Drive folder is empty. Nothing to sync.")
        return
    print("Files synchronized")
    return


if __name__ == "__main__":
    main()
