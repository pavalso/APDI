"""
This module contains the Client class and its dependencies.
"""

from adiauthcli import client

try:
    from entities.blob import Blob, _DBBlob
    from objects._perms import Visibility
except ImportError:
    from src.entities.blob import Blob, _DBBlob
    from src.objects._perms import Visibility


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
        super().__init__("http://localhost:5000", admin_token)

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
    def login(username: str, password: str) -> _LoggedClient:
        """
        Logs in a user.

        Args:
            username: A string representing the username of the client.
            password: A string representing the password of the client.

        Returns:
            A _LoggedClient object representing the logged in client.
        """
        _c = _LoggedClient()

        _c.login(username, password)

        return _c

    @staticmethod
    def fetch_user(token: str) -> _LoggedClient:
        """
        Fetches a user.

        Args:
            token: A string representing the token of the user.

        Returns:
            A Client object representing the fetched user.
        """
        _c = _LoggedClient()

        username = _c.token_owner(token)

        _c._user_ = username
        _c._token_ = token

        return _c