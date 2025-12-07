import sqlite3
from typing import List
from .base_repository import BaseRepository
from ..models.event import Event
from ..logging_config import get_logger

logger = get_logger(__name__)

class EventRepository(BaseRepository):
    def __init__(self, connection: sqlite3.Connection):
        super().__init__(connection)

    def add(self, event: Event) -> None:
        cursor = self._conn.cursor()
        cursor.execute(
            """
            INSERT INTO events
            (id, name, date, time, category, description, duration_minutes, venue_id, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event.id,
                event.name,
                event.date,
                event.time,
                event.category,
                event.description,
                event.duration_minutes,
                event.venue_id,
                1 if event.is_active else 0
            )
        )
        self._conn.commit()
        #logger.info("Event created: %s", event.display_info())

    def get_all(self) -> List[Event]:
        cursor = self._conn.cursor()
        cursor.execute(
            """
            SELECT id, name, date, time, category, description,
                   duration_minutes, venue_id, is_active
            FROM events
            """
        )
        rows = cursor.fetchall()
        events: List[Event] = []
        for row in rows:
            events.append(
                Event(
                    id=row[0],
                    name=row[1],
                    date=row[2],
                    time=row[3],
                    category=row[4],
                    description=row[5],
                    duration_minutes=row[6],
                    venue_id=row[7],
                    is_active=bool(row[8])
                )
            )
        #logger.info("Fetched %d events from database.", len(events))
        return events
    
    def get_by_id(self, event_id: str) -> Event | None:
        cursor = self._conn.cursor()
        cursor.execute(
            """
            SELECT id, name, date, time, category, description,
                   duration_minutes, venue_id, is_active
            FROM events
            WHERE id = ?
            """,
            (event_id,)
        )
        row = cursor.fetchone()
        if row is None:
            return None

        return Event(
            id=row[0],
            name=row[1],
            date=row[2],
            time=row[3],
            category=row[4],
            description=row[5],
            duration_minutes=row[6],
            venue_id=row[7],
            is_active=bool(row[8]),
        )
    
    def update(self, event: Event) -> None:
        cursor = self._conn.cursor()
        cursor.execute(
            """
            UPDATE events
            SET name = ?, date = ?, time = ?, category = ?, description = ?,
                duration_minutes = ?, venue_id = ?, is_active = ?
            WHERE id = ?
            """,
            (
                event.name,
                event.date,
                event.time,
                event.category,
                event.description,
                event.duration_minutes,
                event.venue_id,
                int(event.is_active),
                event.id,
            )
        )
        self._conn.commit()
        #logger.info("Event updated: %s", event.display_info())

    def delete_by_id(self, event_id: str) -> bool:
        cursor = self._conn.cursor()
        cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
        self._conn.commit()
        deleted = cursor.rowcount > 0
        if deleted:
            logger.info("Event deleted: id=%s", event_id)
        else:
            logger.warning("Event not found for delete: id=%s", event_id)
        return deleted
