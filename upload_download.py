from file_check import create_service, list_files_drive, date_check
from credentials.path import MAP_PATH

from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from googleapiclient.errors import HttpError


def download_files(service, file_list):
    try:
        for item in file_list:
            request = service.files().get_media(fileId=item["id"])
            file = open(f"{MAP_PATH}\\{item["name"]}", "wb")
            downloader = MediaIoBaseDownload(file, request)

            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Downloading {item["name"]}\nDownload {int(status.progress() * 100)}.")

            file.close()

    except HttpError as error:
        print(f"An error occurred during download: {error}")


def upload_files(service, file_list, path):
    try:
        for item in file_list:
            media = MediaFileUpload(
                f"{path}//{item["name"]}",
                resumable=True,
            )
            service.files().update(fileId=f"{item["id"]}", media_body=media).execute()
            print(f"uploading {item["name"]}")

    except HttpError as error:
        print(f"An error occurred during upload: {error}")
