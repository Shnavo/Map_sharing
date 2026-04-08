from auth import get_credentials
from credentials.path import PATH
import datetime as dt
import os

from googleapiclient.discovery import build


def list_files_drive():
    creds = get_credentials()
    service = build("drive", "v3", credentials=creds)
    file_list = (
        service.files()
        .list(
            q="name contains 'Sosnowiec'",
            pageSize=10,
            fields="nextPageToken, files(id, name, modifiedTime, createdTime)",
        )
        .execute()
    )

    items = file_list.get("files", [])

    if not items:
        print("Nie znaleziono plików.")
    else:
        print("Pliki:")
        for item in items:
            print(
                f"{item['name']} ({item['id']}) modified: {item['modifiedTime']} created: {item['createdTime']}"
            )
            google = dt.datetime.strptime(item["modifiedTime"], "%Y-%m-%dT%H:%M:%S.%fZ")
            drive = dt.datetime.fromtimestamp(os.path.getctime(PATH))
            if google > drive:
                print("google bigger")
            else:
                print("drive bigger")


if __name__ == "__main__":
    list_files_drive()
