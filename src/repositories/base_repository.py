import sqlite3
from ..logging_config import get_logger

logger = get_logger(__name__)

class BaseRepository:
    def __init__(self, connection: sqlite3.Connection):
        self._conn = connection
