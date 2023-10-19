"""
This module defines the Perms class and the Visibility enumeration.
"""

from enum import IntFlag
from dataclasses import dataclass


class Visibility(IntFlag):
    """
    An enumeration representing the visibility of a permission.
    """
    PUBLIC = 1
    PRIVATE = 2

    def __str__(self) -> str:
        return self.name.lower()

@dataclass
class _Perms:
    """
    A class representing the permissions of an entity.
    """

    def __init__(self, owner: str, visibility: Visibility) -> None:
        """
        Initializes a new instance of the Perms class.

        Args:
            owner: The owner of the entity.
            visibility: The visibility of the entity.
            allowed_users: The set of users allowed to access the entity.
        """
        self.owner = owner
        self.visibility = Visibility(visibility)

__export__ = (_Perms,)
