try:
    from db.dao import DAO
    from blob import Blob
except ImportError:
    from src.db.dao import DAO
    from src.blob import Blob


if __name__ == '__main__':
    DAO.connect('pyblob.db')
    Blob.create('test')
