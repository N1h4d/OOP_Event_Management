import sqlite3
from ..logging_config import get_logger

logger = get_logger(__name__)

def initialize_database(conn: sqlite3.Connection):
    
    cursor = conn.cursor()

    # Venue
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS venues (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            capacity INTEGER NOT NULL,
            manager_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            is_open INTEGER NOT NULL DEFAULT 1
        )
        """
    )

    # Event
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            duration_minutes INTEGER NOT NULL,
            venue_id TEXT NOT NULL,
            is_active INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (venue_id) REFERENCES venues(id)
        )
        """
    )

    # Participant
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS participants (
            id TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            registration_date TEXT NOT NULL,
            is_vip INTEGER NOT NULL DEFAULT 0
        )
        """
    )

    # Ticket
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tickets (
            id TEXT PRIMARY KEY,
            event_id TEXT NOT NULL,
            participant_id TEXT NOT NULL,
            price REAL NOT NULL,
            seat_number TEXT NOT NULL,
            ticket_type TEXT NOT NULL,
            purchase_date TEXT NOT NULL,
            is_used INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (event_id) REFERENCES events(id),
            FOREIGN KEY (participant_id) REFERENCES participants(id)
        )
        """
    )

    conn.commit()
    logger.info("Database schema initialized successfully.")
