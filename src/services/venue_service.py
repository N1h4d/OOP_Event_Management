from typing import List

from ..models.venue import Venue
from ..repositories.venue_repository import VenueRepository
from ..logging_config import get_logger
from .base_service import BaseService

logger = get_logger(__name__)


class VenueService(BaseService):
    def __init__(self, repository: VenueRepository):
        super().__init__(repository)

    # ✅ CREATE
    def create_venue(
        self,
        name: str,
        address: str,
        capacity: int,
        manager_name: str,
        phone: str,
        is_open: bool = True
    ) -> Venue:
        """
        Creates a Venue domain object, applies basic validation
        and saves it using the repository.
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive.")

        venue = Venue(
            name=name,
            address=address,
            capacity=capacity,
            manager_name=manager_name,
            phone=phone,
            is_open=is_open
        )

        self.repository.add(venue)

        # ✅ LOG — YALNIZ SERVICE SƏVİYYƏSİ
        logger.info("Venue created: id=%s, name=%s", venue.id, venue.name)

        return venue

    # ✅ READ (LIST)
    def list_venues(self) -> List[Venue]:
        """
        Returns all venues from the database.
        """
        venues = self.repository.get_all()

        # ✅ BU LOG QALA BİLƏR (istəsən silə də bilərsən)
        logger.info("Retrieved %d venues.", len(venues))

        return venues

    # ✅ UPDATE
    def update_venue(
        self,
        venue_id: str,
        name: str,
        address: str,
        capacity: int,
        manager_name: str,
        phone: str,
        is_open: bool
    ) -> Venue:
        venue = self.repository.get_by_id(venue_id)
        if venue is None:
            raise ValueError("Venue not found.")

        if capacity <= 0:
            raise ValueError("Capacity must be positive.")

        venue._name = name
        venue._address = address
        venue._capacity = capacity
        venue._manager_name = manager_name
        venue._phone = phone
        venue._is_open = is_open

        self.repository.update(venue)

        # ✅ LOG — UPDATE
        logger.info("Venue updated: id=%s, name=%s", venue.id, venue.name)

        return venue
    
    # ✅ DELETE
    def delete_venue(self, venue_id: str) -> bool:
        deleted = self.repository.delete_by_id(venue_id)
        if not deleted:
            raise ValueError("Venue not found.")

        # ✅ LOG — DELETE
        logger.info("Venue deleted: id=%s", venue_id)

        return True
