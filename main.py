from file_check import *
from upload_download import download_files, upload_files
import os


def main():
    """
    Orchestrates the map synchronization process between local storage and Google Drive.

    The workflow follows these steps:
    1. Authenticates the user and initializes the Google Drive service.
    2. Fetches metadata for specific map files from a predefined Google Drive folder.
    3. Compares cloud timestamps with local file timestamps using a 20-second tolerance.
    4. Decides on the required action:
        - Uploads local files if they are newer.
        - Downloads cloud files if they are newer.
        - Skips if files are synchronized or if the cloud folder is empty.

    Execution flow is managed via the 'date_check' logic to prevent unnecessary data transfer.
    """
    if not os.path.isfile(os.path.abspath("credentials.json")):
        setup_creds()
    drive_id, path = startup()
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
        raise Exception("missing files in Google folder")
    print("Files synchronized")
    return


if __name__ == "__main__":
    main()
