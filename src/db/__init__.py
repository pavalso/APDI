"""
This module contains the database package for the APDI application.
"""

from . import _dao

_DAO = _dao.DAO

connect = _DAO.connect
close = _DAO.close

__all__ = ['_DAO', 'connect', 'close']
