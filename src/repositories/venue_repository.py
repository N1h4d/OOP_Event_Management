import sqlite3
from typing import List
from .base_repository import BaseRepository
from ..models.venue import Venue
from ..logging_config import get_logger

logger = get_logger(__name__)

class VenueRepository(BaseRepository):
    def __init__(self, connection: sqlite3.Connection):
        super().__init__(connection)

    def add(self, venue: Venue) -> None:
        cursor = self._conn.cursor()
        cursor.execute(
            """
            INSERT INTO venues (id, name, address, capacity, manager_name, phone, is_open)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                venue.id,
                venue.name,
                venue.address,
                venue.capacity,
                venue.manager_name,
                venue.phone,
                1 if venue.is_open else 0
            )
        )
        self._conn.commit()
        #logger.info("Venue created: %s", venue.display_info())

    def get_all(self) -> List[Venue]:
        cursor = self._conn.cursor()
        cursor.execute(
            "SELECT id, name, address, capacity, manager_name, phone, is_open FROM venues"
        )
        rows = cursor.fetchall()
        venues: List[Venue] = []
        for row in rows:
            venues.append(
                Venue(
                    id=row[0],
                    name=row[1],
                    address=row[2],
                    capacity=row[3],
                    manager_name=row[4],
                    phone=row[5],
                    is_open=bool(row[6])
                )
            )
        #logger.info("Fetched %d venues from database.", len(venues))
        return venues
    
    def get_by_id(self, venue_id: str) -> Venue | None:
        cursor = self._conn.cursor()
        cursor.execute(
            """
            SELECT id, name, address, capacity, manager_name, phone, is_open
            FROM venues
            WHERE id = ?
            """,
            (venue_id,)
        )
        row = cursor.fetchone()
        if row is None:
            return None

        return Venue(
            id=row[0],
            name=row[1],
            address=row[2],
            capacity=row[3],
            manager_name=row[4],
            phone=row[5],
            is_open=bool(row[6]),
        )
    
    def update(self, venue: Venue) -> None:
        cursor = self._conn.cursor()
        cursor.execute(
            """
            UPDATE venues
            SET name = ?, address = ?, capacity = ?, manager_name = ?, phone = ?, is_open = ?
            WHERE id = ?
            """,
            (
                venue.name,
                venue.address,
                venue.capacity,
                venue.manager_name,
                venue.phone,
                int(venue.is_open),
                venue.id,
            )
        )
        self._conn.commit()
        #logger.info("Venue updated: %s", venue.display_info())

    def delete_by_id(self, venue_id: str) -> bool:
        cursor = self._conn.cursor()
        cursor.execute("DELETE FROM venues WHERE id = ?", (venue_id,))
        self._conn.commit()
        deleted = cursor.rowcount > 0
        if deleted:
            logger.info("Venue deleted: id=%s", venue_id)
        else:
            logger.warning("Venue not found for delete: id=%s", venue_id)
        return deleted
