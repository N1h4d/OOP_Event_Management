from typing import List

from ..models.participant import Participant
from ..repositories.participant_repository import ParticipantRepository
from ..logging_config import get_logger
from .base_service import BaseService

logger = get_logger(__name__)


class ParticipantService(BaseService):
    def __init__(self, repository: ParticipantRepository):
        super().__init__(repository)

    # ✅ CREATE
    def create_participant(
        self,
        full_name: str,
        email: str,
        phone: str,
        age: int,
        gender: str,
        registration_date: str,
        is_vip: bool = False
    ) -> Participant:
        """
        Creates a Participant and saves it.
        """
        if age <= 0:
            raise ValueError("Age must be positive.")

        participant = Participant(
            full_name=full_name,
            email=email,
            phone=phone,
            age=age,
            gender=gender,
            registration_date=registration_date,
            is_vip=is_vip
        )

        self.repository.add(participant)

        # ✅ SADƏ, BİZNES SƏVİYYƏLİ LOG
        logger.info(
            "Participant created: id=%s, name=%s",
            participant.id,
            participant.full_name
        )

        return participant

    # ✅ READ (LIST)
    def list_participants(self) -> List[Participant]:
        participants = self.repository.get_all()

        logger.info("Retrieved %d participants.", len(participants))

        return participants
    
    # ✅ UPDATE
    def update_participant(
        self,
        participant_id: str,
        full_name: str,
        email: str,
        phone: str,
        age: int,
        gender: str,
        registration_date: str,
        is_vip: bool
    ) -> Participant:
        participant = self.repository.get_by_id(participant_id)
        if participant is None:
            raise ValueError("Participant not found.")

        if age <= 0:
            raise ValueError("Age must be positive.")

        participant._full_name = full_name
        participant._email = email
        participant._phone = phone
        participant._age = age
        participant._gender = gender
        participant._registration_date = registration_date
        participant._is_vip = is_vip

        self.repository.update(participant)

        # ✅ UPDATE LOG
        logger.info(
            "Participant updated: id=%s, name=%s",
            participant.id,
            participant.full_name
        )

        return participant
    
    # ✅ DELETE
    def delete_participant(self, participant_id: str) -> bool:
        deleted = self.repository.delete_by_id(participant_id)
        if not deleted:
            raise ValueError("Participant not found.")

        # ✅ DELETE LOG
        logger.info("Participant deleted: id=%s", participant_id)

        return True
