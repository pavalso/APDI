from src import services
from src.objects import Visibility
from src.db import connect
from src.entities import Blob, Client
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
#
#    _bytes = b'123456' * 1000
#
#    _blob = _FileBlob('123456')
#
#    _blob.write(_bytes)
#
#    assert _blob.read() == _bytes
#
#    _blob2 = _FileBlob('123456')
#
#    _blob2.write(b'Buenas')
#
#    print(_blob.read())
#
    with connect('pyapdi.db') as db:

        client2 = Client.login('Toni', 'From the gang')
        client = Client.login('The One', 'From the gang')

        blob = client.create_blob(Visibility.PUBLIC)

        blob.add_permissions(client2.username)

        blob = Blob.fetch(blob.id_)

        print(blob.get_user_permissions(client2.username))
