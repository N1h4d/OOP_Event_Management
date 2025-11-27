import sqlite3
from typing import List
from .base_repository import BaseRepository
from ..models.ticket import Ticket
from ..logging_config import get_logger

logger = get_logger(__name__)

class TicketRepository(BaseRepository):
    def __init__(self, connection: sqlite3.Connection):
        super().__init__(connection)

    def add(self, ticket: Ticket) -> None:
        cursor = self._conn.cursor()
        cursor.execute(
            """
            INSERT INTO tickets
            (id, event_id, participant_id, price, seat_number,
             ticket_type, purchase_date, is_used)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                ticket.id,
                ticket.event_id,
                ticket.participant_id,
                ticket.price,
                ticket.seat_number,
                ticket.ticket_type,
                ticket.purchase_date,
                1 if ticket.is_used else 0
            )
        )
        self._conn.commit()
        logger.info("Ticket created: %s", ticket.display_info())

    def get_all(self) -> List[Ticket]:
        cursor = self._conn.cursor()
        cursor.execute(
            """
            SELECT id, event_id, participant_id, price,
                   seat_number, ticket_type, purchase_date, is_used
            FROM tickets
            """
        )
        rows = cursor.fetchall()
        tickets: List[Ticket] = []
        for row in rows:
            tickets.append(
                Ticket(
                    id=row[0],
                    event_id=row[1],
                    participant_id=row[2],
                    price=row[3],
                    seat_number=row[4],
                    ticket_type=row[5],
                    purchase_date=row[6],
                    is_used=bool(row[7])
                )
            )
        logger.info("Fetched %d tickets from database.", len(tickets))
        return tickets
