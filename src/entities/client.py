"""
This module contains the Client class and its dependencies.
"""

try:
    from entities.blob import Blob, _DBBlob
    from objects._perms import Visibility
except ImportError:
    from src.entities.blob import Blob, _DBBlob
    from src.objects._perms import Visibility


class _LoggedClient:
    """
    A wrapper class for the client class.
    """

    @property
    def blobs(self) -> list[Blob]:
        """
        Fetches all the blobs for the current user.

        Returns:
            A list of Blob objects.
        """
        return Blob.fetch_user_blobs(self.username)

    def __init__(self, username: str, password: str) -> None:
        """
        Initializes a new instance of the _LoggedClient class.

        Args:
            username: A string representing the username of the client.
            password: A string representing the password of the client.
        """
        self.username = username
        self.password = password

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
        return _LoggedClient(username, password)

    @staticmethod
    def fetch_user(token: str) -> _LoggedClient:
        """
        Fetches a user.

        Args:
            token: A string representing the token of the user.

        Returns:
            A Client object representing the fetched user.
        """
        raise NotImplementedError

    @staticmethod
    def create_user(username: str, password: str) -> _LoggedClient:
        """
        Creates a new user.

        Args:
            username: A string representing the username of the new user.
            password: A string representing the password of the new user.

        Returns:
            A Client object representing the newly created user.
        """
        raise NotImplementedError

    @staticmethod
    def delete_user(username: str) -> None:
        """
        Deletes a user.

        Args:
            username: A string representing the username of the user to be deleted.
        """
        raise NotImplementedError

    @staticmethod
    def update_user(username: str, password: str) -> _LoggedClient:
        """
        Updates a user.

        Args:
            username: A string representing the username of the user to be updated.
            password: A string representing the new password of the user.

        Returns:
            A Client object representing the updated user.
        """
        raise NotImplementedError
