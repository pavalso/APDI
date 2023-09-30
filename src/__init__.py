try:
    from db import new_blob
except ImportError:
    from src.db import new_blob


print(new_blob('me').id)
