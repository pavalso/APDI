import uuid

from .dao import DAO

try:
    from src.classes.file_blob import FileBlob
except ImportError:
    from classes.file_blob import FileBlob


def new_blob(owner: str, public: bool = False, allowedUsers: list = None) -> FileBlob:
    _b = FileBlob(str(uuid.uuid4()), owner, public, allowedUsers)
    DAO.newBlob(_b.id, _b.owner, _b.public)
    return _b

def update_blob(blob_id, new_blob: FileBlob) -> None:
    DAO.updateBlob(blob_id, new_blob.owner, new_blob.public)

def delete_blob(blob_id) -> None:
    DAO.deleteBlob(blob_id)


