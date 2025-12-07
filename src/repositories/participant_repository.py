import sqlite3
from typing import List
from .base_repository import BaseRepository
from ..models.participant import Participant
from ..logging_config import get_logger

logger = get_logger(__name__)

class ParticipantRepository(BaseRepository):
    def __init__(self, connection: sqlite3.Connection):
        super().__init__(connection)

    def add(self, participant: Participant) -> None:
        cursor = self._conn.cursor()
        cursor.execute(
            """
            INSERT INTO participants
            (id, full_name, email, phone, age, gender, registration_date, is_vip)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                participant.id,
                participant.full_name,
                participant.email,
                participant.phone,
                participant.age,
                participant.gender,
                participant.registration_date,
                1 if participant.is_vip else 0
            )
        )
        self._conn.commit()
        #logger.info("Participant created: %s", participant.display_info())

    def get_all(self) -> List[Participant]:
        cursor = self._conn.cursor()
        cursor.execute(
            """
            SELECT id, full_name, email, phone, age, gender, registration_date, is_vip
            FROM participants
            """
        )
        rows = cursor.fetchall()
        participants: List[Participant] = []
        for row in rows:
            participants.append(
                Participant(
                    id=row[0],
                    full_name=row[1],
                    email=row[2],
                    phone=row[3],
                    age=row[4],
                    gender=row[5],
                    registration_date=row[6],
                    is_vip=bool(row[7])
                )
            )
        #logger.info("Fetched %d participants from database.", len(participants))
        return participants
    
    def get_by_id(self, participant_id: str) -> Participant | None:
        cursor = self._conn.cursor()
        cursor.execute(
            """
            SELECT id, full_name, email, phone, age, gender,
                   registration_date, is_vip
            FROM participants
            WHERE id = ?
            """,
            (participant_id,)
        )
        row = cursor.fetchone()
        if row is None:
            return None

        return Participant(
            id=row[0],
            full_name=row[1],
            email=row[2],
            phone=row[3],
            age=row[4],
            gender=row[5],
            registration_date=row[6],
            is_vip=bool(row[7]),
        )
    
    def update(self, participant: Participant) -> None:
        cursor = self._conn.cursor()
        cursor.execute(
            """
            UPDATE participants
            SET full_name = ?, email = ?, phone = ?, age = ?, gender = ?,
                registration_date = ?, is_vip = ?
            WHERE id = ?
            """,
            (
                participant.full_name,
                participant.email,
                participant.phone,
                participant.age,
                participant.gender,
                participant.registration_date,
                int(participant.is_vip),
                participant.id,
            )
        )
        self._conn.commit()
        #logger.info("Participant updated: %s", participant.display_info())

    def delete_by_id(self, participant_id: str) -> bool:
        cursor = self._conn.cursor()
        cursor.execute("DELETE FROM participants WHERE id = ?", (participant_id,))
        self._conn.commit()
        deleted = cursor.rowcount > 0
        if deleted:
            logger.info("Participant deleted: id=%s", participant_id)
        else:
            logger.warning("Participant not found for delete: id=%s", participant_id)
        return deleted
