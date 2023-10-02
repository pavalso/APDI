from src import services
from src.objects import Visibility
from src.db import connect

connect('pyapdi.db')

blob = services.get_blob('9bdb2341-7c05-4289-a4b0-2b17ac5cced5')

blob.open()

print(hash(blob), blob.read())
