from src import services
from src.objects import Visibility
from src.db import connect
from src.entities import Blob

if __name__ == '__main__':
    connect('pyapdi.db')

    blob = services.get_blob('9bdb2341-7c05-4289-a4b0-2b17ac5cced5')

    print(hash(blob), blob.read())

    blob.write(b'Hasta la vista, baby!')

    _blob = Blob('9bdb2341-7c05-4289-a4b0-2b17ac5cced5', 'me')

    print(hash(_blob), _blob.read())
