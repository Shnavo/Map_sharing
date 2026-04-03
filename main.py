from auth import get_credentials

from googleapiclient.discovery import build


def list_files():
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


if __name__ == "__main__":
    list_files()
