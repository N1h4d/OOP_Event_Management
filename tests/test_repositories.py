import unittest
import sqlite3

from src.database.schema import initialize_database
from src.models.venue import Venue
from src.repositories.venue_repository import VenueRepository
from src.services.venue_service import VenueService


class VenueServiceTests(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        initialize_database(self.conn)

        repo = VenueRepository(self.conn)
        self.service = VenueService(repo)

    def tearDown(self):
        self.conn.close()

    def test_create_update_delete_venue(self):
        venue = self.service.create_venue(
            name="Test Hall",
            address="Test Street 1",
            capacity=100,
            manager_name="John Doe",
            phone="1234567",
            is_open=True
        )

        self.assertIsNotNone(venue.id)
        self.assertEqual(venue.capacity, 100)

        # UPDATE
        updated = self.service.update_venue(
            venue_id=venue.id,
            name="Updated Hall",
            address="New Address",
            capacity=150,
            manager_name="Jane Doe",
            phone="7654321",
            is_open=False
        )

        self.assertEqual(updated.name, "Updated Hall")
        self.assertEqual(updated.capacity, 150)
        self.assertFalse(updated.is_open)

        # DELETE
        deleted = self.service.delete_venue(venue.id)
        self.assertTrue(deleted)


if __name__ == "__main__":
    unittest.main()
