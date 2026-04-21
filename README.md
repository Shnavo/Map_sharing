# Google Drive Map Synchronizer

Python-based script created by the need to share Valheim map files between multiple people. The script compares modification timestamps to decide whether to upload local changes to the cloud or download updates to the local machine.

## Features
- Two-Way Synchronization: Compares modification times between local and remote files.
- Binary File Support: Safely handles uploads and downloads of large database files without corruption.
- Error Resilience: Utilizes resumable upload mode to handle network interruptions gracefully.
- Automatic Authorization: Implements OAuth 2.0 flow (Google Drive API v3) for secure access.

## Requirements
- Python 3.10+
- A Google Account with access to the Google Cloud Console.

## Quick Start
### Google Cloud Setup
- Create a project in the Google Cloud Console.
- Enable the Google Drive API.
- Configure the OAuth Consent Screen and add the following scope: https://www.googleapis.com/auth/drive.
- Generate OAuth Client ID Credentials (select "Desktop App") and download the JSON file. Rename it to credentials.json and place it in the **credentials** folder.

### Install Dependencies
Install the required libraries using pip:

		pip install requirements.txt
		
### Configuration
Set the path to your maps folder within the path.py file in credentials folder:

		MAP_PATH = "C:/Path/To/Your/Maps"

### Usage
On the first run, a browser window will open asking for Google account authorization. Once granted, a token.json file will be created, allowing the script to run automatically in the future without manual login.

## Sync Logic Explained
The program follows a strict logic based on the modifiedTime field:
- Upload: Triggered if the local file is newer than the Google Drive version by more than a 20-second margin.
- Download: Triggered if the Google Drive version is newer than the local fileby more than a 20-second margin.
- Idle: No action is taken if the timestamps are within the tolerance window (handling server-side time drift).

## TO-DO
- [ ]**TYPEHINTING!!!**
- [ ]create a first time launch setup for putting in correct paths
- [ ]create a simple UI to show what's going on
- [x]Initial release with OAuth2 support
