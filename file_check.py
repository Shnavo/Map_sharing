from authentication import get_credentials
from credentials.path import MAP_PATH, DRIVE_ID
import datetime as dt
import os

from googleapiclient.discovery import build


def create_service():
    creds = get_credentials()
    service = build("drive", "v3", credentials=creds)
    return service


def list_files_drive(service):
    file_list = (
        service.files()
        .list(
            q=f"'{DRIVE_ID}' in parents",  # change to insertable info
            pageSize=10,
            fields="nextPageToken, files(id, name, modifiedTime, createdTime)",
        )
        .execute()
    )

    return file_list.get("files", [])


def date_check(file_list):
    file = file_list[0]
    if not file_list:
        return "missing"
    else:
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

        # print("Files:")
        # for item in file_list:
        #     print(
        #         f"{item['name']} ({item['id']}) modified: {item['modifiedTime']} created: {item['createdTime']}"
        #     )
