import os
import zipfile

from google_auth_oauthlib.flow import Flow

dysk = os.path.getmtime("C:\\Users\\szang\\AppData\\LocalLow\\IronGate\\Valheim\\worlds_local\\Sosnowiec.db")
with zipfile.ZipFile("C:\\Users\\szang\\Downloads\\drive-download-20260304T111228Z-1-001.zip") as zip:
    zip.extractall("C:\\Users\\szang\\Downloads\\maps")
google = os.path.getmtime("C:\\Users\\szang\\Downloads\\maps\\Sosnowiec.db")
if (dysk > google):
    print (f"na dysku: {dysk}")
elif (dysk < google):
    print(f"na google: {google}")
else:
    print("equal")