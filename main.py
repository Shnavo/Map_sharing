from file_check import create_service, list_files_drive, date_check
from upload_download import download_files, upload_files
from credentials.path import MAP_PATH


def main():
    service = create_service()
    file_list = list_files_drive(service)
    action = date_check(file_list)
    if action == "download":
        download_files(service, file_list)
        return
    if action == "upload":
        upload_files(service, file_list, MAP_PATH)
        return
    if action == "missing":
        raise Exception("missing files in Google folder")
    print("Files synchronized")
    return


if __name__ == "__main__":
    main()
