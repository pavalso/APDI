try:
    import exceptions
    from db.dao import DAO
    from src.db.dbblob import Blob
except ImportError:
    from src import exceptions
    from src.db.dao import DAO
    from src.db.dbblob import Blob


if __name__ == '__main__':
    DAO.connect('pyblob.db')
