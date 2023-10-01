"""
This module contains the main entry point for the APDI application.
"""

try:
    import exceptions
    from db.dao import DAO
    from entity import Blob, Visibility
except ImportError:
    from src import exceptions
    from src.db.dao import DAO
    from src.entity import Blob, Visibility


if __name__ == '__main__':
    DAO.connect('pyblob.db')
