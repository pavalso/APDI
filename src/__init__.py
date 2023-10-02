"""
This module contains the main entry point for the APDI application.
"""

try:
    import exceptions
    import objects
    import entities
    import db
except ImportError:
    from src import exceptions
    from src import objects
    from src import entities
    from src import db

__all__ = ['exceptions', 'objects', 'entities', 'db']
