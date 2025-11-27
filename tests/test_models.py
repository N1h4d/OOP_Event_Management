import unittest

from src.models.event import Event
from src.models.venue import Venue
from src.models.participant import Participant
from src.models.ticket import Ticket


class TestModels(unittest.TestCase):

    def test_event_creation(self):
        event = Event(
            name="Test Event",
            date="2025-12-31",
            time="20:00",
            category="Concert",
            description="New Year concert",
            duration_minutes=120,
            venue_id="venue-123"
        )
        self.assertEqual(event.name, "Test Event")
        self.assertEqual(event.date, "2025-12-31")
        self.assertEqual(event.time, "20:00")
        self.assertEqual(event.category, "Concert")
        self.assertEqual(event.duration_minutes, 120)
        self.assertEqual(event.venue_id, "venue-123")
        self.assertIsNotNone(event.id)

    def test_venue_creation(self):
        venue = Venue(
            name="Main Hall",
            address="Baku Center",
            capacity=500,
            manager_name="John Doe",
            phone="+994501112233"
        )
        self.assertEqual(venue.name, "Main Hall")
        self.assertEqual(venue.capacity, 500)
        self.assertTrue(venue.is_open)

    def test_participant_creation(self):
        participant = Participant(
            full_name="Alice Smith",
            email="alice@example.com",
            phone="+994501234567",
            age=25,
            gender="F",
            registration_date="2025-01-01",
            is_vip=True
        )
        self.assertEqual(participant.full_name, "Alice Smith")
        self.assertEqual(participant.email, "alice@example.com")
        self.assertTrue(participant.is_vip)

    def test_ticket_creation(self):
        ticket = Ticket(
            event_id="event-1",
            participant_id="part-1",
            price=50.0,
            seat_number="A10",
            ticket_type="VIP",
            purchase_date="2025-02-02"
        )
        self.assertEqual(ticket.event_id, "event-1")
        self.assertEqual(ticket.seat_number, "A10")
        self.assertEqual(ticket.ticket_type, "VIP")
        self.assertFalse(ticket.is_used)


if __name__ == "__main__":
    unittest.main()
