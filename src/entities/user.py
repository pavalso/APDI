"""
This module contains the User class which provides methods for interacting with the 
authentication server.
"""


from auth_client.adiauthcli import client

from src.exceptions import UserAlreadyExistsError, UserNotFoundError


_admin_client = client.Client(
    "http://localhost:5000",
    "admin")

def _refresh_token(f):
    def _wrapper(*args, **kwargs) -> None:
        try:
            _r = f(*args, **kwargs)
        except client.Unauthorized:
            _admin_client.refresh_token()
            _r = f(*args, **kwargs)
        return _r
    return _wrapper

class User:
    """
    The User class provides methods for interacting with the authentication server.
    """

    @_refresh_token
    @staticmethod
    def token_owner(token: str) -> str:
        """
        Returns the username of the owner of the given token.

        Args:
            token: The token to check ownership of.

        Returns:
            str: The username of the token owner.
        """
        try:
            return _admin_client.token_owner(token)
        except client.UserNotExists:
            return None

    @_refresh_token
    @staticmethod
    def user_exists(username: str) -> bool:
        """
        Checks if a user with the given username exists.

        Args:
            username: The username to check.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        return _admin_client.user_exists(username)

    @_refresh_token
    @staticmethod
    def new_user(username: str, password: str) -> None:
        """
        Creates a new user with the given username and password.

        Args:
            username: The username of the new user.
            password: The password of the new user.
        """
        try:
            return _admin_client.new_user(username, password)
        except client.UserAlreadyExists as e:
            raise UserAlreadyExistsError from e

    @_refresh_token
    @staticmethod
    def delete_user(username: str) -> None:
        """
        Deletes the user with the given username.

        Args:
            username: The username of the user to delete.
        """
        try:
            return _admin_client.delete_user(username)
        except client.UserNotExists as e:
            raise UserNotFoundError(username) from e

    @_refresh_token
    @staticmethod
    def update_user(username: str, password: str) -> None:
        """
        Updates the password of the user with the given username.

        Args:
            username: The username of the user to update.
            password: The new password for the user.
        """
        try:
            return _admin_client.set_user_password(username, password)
        except client.UserNotExists as e:
            raise UserNotFoundError(username) from e
