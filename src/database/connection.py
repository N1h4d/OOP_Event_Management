import sqlite3
from typing import Optional

class DatabaseConnection:
    """
    Singleton pattern – layihə boyu eyni DB bağlantısından istifadə edirik.
    """
    _instance: Optional["DatabaseConnection"] = None

    def __new__(cls, db_path: str = "event_management.db"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._db_path = db_path
            cls._instance._conn = sqlite3.connect(db_path)
        return cls._instance

    @property
    def connection(self) -> sqlite3.Connection:
        return self._conn

    def close(self):
        if self._conn:
            self._conn.close()
            DatabaseConnection._instance = None
