from src import services
from src.objects import Visibility
from src.db import connect
from src.entities import Blob
from src.objects import _FileBlob


if __name__ == '__main__':
#    connect('pyapdi.db')
#
#    blob = services.get_blob('9bdb2341-7c05-4289-a4b0-2b17ac5cced5')
#
#    print(hash(blob), blob.read())
#
#    blob.write(b'Hasta la vista, baby!')
#
#    _blob = Blob('9bdb2341-7c05-4289-a4b0-2b17ac5cced5', 'me')
#
#    print(hash(_blob), _blob.read())

    _bytes = b'123456' * 1000

    _blob = _FileBlob('123456')

    _blob.write(_bytes)

    assert _blob.read() == _bytes
