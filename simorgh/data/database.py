__author__ = 'mpwd'

import os
from tinydb import TinyDB
from tinydb.storages import MemoryStorage

default_db_file = os.path.join(os.path.expanduser('~'), ".simorgh_db.json")

if 'SIMORGH_DB' in os.environ:
    if os.environ['SIMORGH_DB'].lower() in [':memory:', ':MEMORY:']:
        db = TinyDB(storage=MemoryStorage)
    else:
        db = TinyDB(os.environ['SIMORGH_DB'])
else:
    db = TinyDB(default_db_file)
