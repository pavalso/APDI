"""
This module contains the Perms class which provides methods for managing permissions.
"""

from src.db._dao import _DAO


class Perms:
    """
    The Perms class provides methods for managing permissions.
    """

    @staticmethod
    def create(blob: str, user: str) -> None:
        """
        Adds permissions for a user to a blob.

        Args:
            blob: The blob to add permissions for.
            user: The user to add permissions for.
        """
        _DAO.add_perms(blob, user)

    @staticmethod
    def delete(blob: str, user: str) -> None:
        """
        Removes permissions for a user from a blob.

        Args:
            blob: The blob to remove permissions from.
            user: The user to remove permissions for.
        """
        _DAO.remove_perms(blob, user)

    @staticmethod
    def exists(blob: str, user: str) -> bool:
        """
        Checks if a user has permissions for a blob.

        Args
            blob: The blob to check permissions for.
            user: The user to check permissions for.
        
        Returns:
            If the user has permissions for the blob.
        """
        return _DAO.get_user_perms(blob, user) is not None

    @staticmethod
    def bulk_create_perms(blob: str, users: set[str]) -> None:
        """
        Adds permissions for multiple users to a blob.

        Args:
            blob: The blob to add permissions for.
            users: The users to add permissions for.
        """
        _DAO.bulk_add_perms(blob, users)

    @staticmethod
    def fetch_blob_perms(blob: str) -> list[str]:
        """
        Gets all users with permissions for a blob.

        Args:
            blob: The blob to get permissions for.

        Returns:
            list[str]: A list of usernames with permissions for the blob.
        """
        _r = _DAO.get_blob_perms(blob)

        return [i[1] for i in _r]

    @staticmethod
    def put_blob_perms(blob: str, users: set[str]) -> None:
        """
        Sets the permissions for a blob.

        Args:
            blob: The blob to set permissions for.
            users: The users to set permissions for.
        """
        _DAO.replace_perms(blob, users)
