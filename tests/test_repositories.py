import unittest
import sqlite3

from src.database.schema import initialize_database
from src.models.venue import Venue
from src.models.event import Event
from src.repositories.venue_repository import VenueRepository
from src.repositories.event_repository import EventRepository


class TestRepositories(unittest.TestCase):

    def setUp(self):
        # Hər test üçün yaddaşda yeni DB
        self.conn = sqlite3.connect(":memory:")
        initialize_database(self.conn)
        self.venue_repo = VenueRepository(self.conn)
        self.event_repo = EventRepository(self.conn)

    def tearDown(self):
        self.conn.close()

    def test_add_and_get_venue(self):
        venue = Venue(
            name="Test Venue",
            address="Test City",
            capacity=100,
            manager_name="Manager",
            phone="000"
        )
        self.venue_repo.add(venue)
        venues = self.venue_repo.get_all()

        self.assertEqual(len(venues), 1)
        self.assertEqual(venues[0].name, "Test Venue")
        self.assertEqual(venues[0].capacity, 100)

    def test_add_and_get_event(self):
        # əvvəl venue yaradırıq
        venue = Venue(
            name="Event Hall",
            address="Baku",
            capacity=300,
            manager_name="Manager",
            phone="111"
        )
        self.venue_repo.add(venue)

        event = Event(
            name="Python Workshop",
            date="2025-10-10",
            time="10:00",
            category="Workshop",
            description="Intro to Python",
            duration_minutes=90,
            venue_id=venue.id
        )
        self.event_repo.add(event)
        events = self.event_repo.get_all()

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].name, "Python Workshop")
        self.assertEqual(events[0].venue_id, venue.id)


if __name__ == "__main__":
    unittest.main()
