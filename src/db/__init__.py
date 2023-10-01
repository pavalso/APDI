"""
This module contains the database package for the APDI application.
"""

from ._dao import _DAO

connect = _DAO.connect
close = _DAO.close

__all__ = ['_DAO', 'connect', 'close']
