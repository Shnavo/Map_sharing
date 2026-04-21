import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from config import SCOPES

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from google.auth.external_account_authorized_user import Credentials as ExtCredentials


def get_credentials() -> Credentials | ExtCredentials:
    """
    Manages OAuth2 credentials by loading an existing token or initiating a login flow.

    The function checks for a local 'token.json'. If missing, invalid, or expired,
    it either refreshes the token or launches a local web server to obtain a new
    authorization code from the user. The resulting token is then cached locally.

    Returns:
        Credentials | ExtCredentials: An authorized credentials object capable
            of refreshing itself or making API calls.

    Raises:
        FileNotFoundError: If the 'credentials.json' file is missing from the
            'credentials/' directory.
    """
    creds = None
    path_to_creds = os.path.join("credentials", "credentials.json")
    path_to_token = os.path.join("credentials", "token.json")

    if os.path.exists(path_to_token):
        creds = Credentials.from_authorized_user_file(path_to_token, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(path_to_creds, SCOPES)
            creds = flow.run_local_server()

        with open(path_to_token, "w") as token:
            token.write(creds.to_json())

    return creds
