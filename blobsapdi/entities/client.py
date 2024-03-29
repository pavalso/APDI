"""
This module contains the Client class and its dependencies.
"""

import os

from adiauthcli import client

from blobsapdi.entities.blob import Blob, _DBBlob
from blobsapdi.enums import Visibility


class _LoggedClient(client.Client):

    @property
    def username(self) -> str:
        """
        Gets the username of the current user.

        Returns:
            A string representing the username of the current user.
        """
        return self._user_

    @property
    def blobs(self) -> dict[str, _DBBlob]:
        """
        Fetches all the blobs for the current user.

        Returns:
            A list of Blob objects.
        """
        return Blob.fetch_user_blobs(self.username)

    def __init__(self, admin_token: str = None) -> None:
        """
        Initializes a new instance of the _LoggedClient class.
        """
        _api = os.getenv("AUTH_API", "http://localhost:3001")

        super().__init__(_api, admin_token, check_service=False)

    def create_blob(self, visibility: Visibility) -> _DBBlob:
        """
        Creates a new blob for the current user.

        Args:
            visibility: A Visibility object representing the visibility of the blob.

        Returns:
            A _DBBlob object representing the newly created blob.
        """
        return Blob.create(self.username, visibility)

class Client:
    """
    A class representing a client.
    """

    @staticmethod
    def check_connection() -> bool:
        """
        Checks the connection to the authentication API.

        Returns:
            A boolean representing the connection status.
        """
        return _LoggedClient().service_up


    @staticmethod
    def fetch_user(token: str) -> _LoggedClient:
        """
        Fetches a user.

        Args:
            token: A string representing the token of the user.

        Returns:
            A Client object representing the fetched user.

        Raises:
            UserNotExists: If the user does not exist.
        """
        _c = _LoggedClient()

        username = _c.token_owner(token)

        _c._user_ = username
        _c._token_ = token

        return _c
