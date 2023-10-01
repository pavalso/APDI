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


if __name__ == '__main__':
    with db.connect('pyblob.db'):
        blob = entities.Blob(1, 'me', objects.Visibility.PRIVATE)

        try:
            entities.Blob.create(blob.id_, blob.perms.owner, blob.perms.visibility)
        except exceptions.BlobAlreadyExistsError:
            entities.Blob.update(blob.id_, owner=blob.perms.owner, visibility=blob.perms.visibility)

        _blob = entities.Blob.fetch(1)

        print(_blob.id_)
