from typing import List

from ..models.event import Event
from ..repositories.event_repository import EventRepository
from ..logging_config import get_logger
from .base_service import BaseService

logger = get_logger(__name__)


class EventService(BaseService):
    def __init__(self, repository: EventRepository):
        super().__init__(repository)

    # ✅ CREATE
    def create_event(
        self,
        name: str,
        date: str,
        time: str,
        category: str,
        description: str,
        duration_minutes: int,
        venue_id: str,
        is_active: bool = True
    ) -> Event:
        """
        Creates an Event, performs basic validation and saves it.
        """
        if duration_minutes <= 0:
            raise ValueError("Duration must be positive.")

        event = Event(
            name=name,
            date=date,
            time=time,
            category=category,
            description=description,
            duration_minutes=duration_minutes,
            venue_id=venue_id,
            is_active=is_active
        )

        self.repository.add(event)

        # ✅ sadə biznes log
        logger.info("Event created: id=%s, name=%s", event.id, event.name)

        return event

    # ✅ READ (LIST)
    def list_events(self) -> List[Event]:
        events = self.repository.get_all()

        logger.info("Retrieved %d events.", len(events))

        return events
    
    # ✅ UPDATE
    def update_event(
        self,
        event_id: str,
        name: str,
        date: str,
        time: str,
        category: str,
        description: str,
        duration_minutes: int,
        venue_id: str,
        is_active: bool
    ) -> Event:
        event = self.repository.get_by_id(event_id)
        if event is None:
            raise ValueError("Event not found.")

        if duration_minutes <= 0:
            raise ValueError("Duration must be positive.")

        event._name = name
        event._date = date
        event._time = time
        event._category = category
        event._description = description
        event._duration_minutes = duration_minutes
        event._venue_id = venue_id
        event._is_active = is_active

        self.repository.update(event)

        # ✅ update log
        logger.info("Event updated: id=%s, name=%s", event.id, event.name)

        return event
    
    # ✅ DELETE
    def delete_event(self, event_id: str) -> bool:
        deleted = self.repository.delete_by_id(event_id)
        if not deleted:
            raise ValueError("Event not found.")

        # ✅ delete log
        logger.info("Event deleted: id=%s", event_id)

        return True
