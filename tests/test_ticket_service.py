import unittest
import sqlite3

from src.database.schema import initialize_database
from src.repositories.ticket_repository import TicketRepository
from src.services.ticket_service import TicketService


class TicketServiceTests(unittest.TestCase):
    def setUp(self):
        # In-memory SQLite DB (file yaratmır)
        self.conn = sqlite3.connect(":memory:")
        initialize_database(self.conn)

        ticket_repo = TicketRepository(self.conn)
        self.ticket_service = TicketService(ticket_repo)

        # Test üçün saxta ID-lər
        self.event_id = "test-event-id"
        self.participant_id = "test-participant-id"

    def tearDown(self):
        self.conn.close()

    def test_standard_pricing(self):
        """
        StandardPricing: final price = base price
        """
        base_price = 100.0
        ticket = self.ticket_service.sell_ticket(
            event_id=self.event_id,
            participant_id=self.participant_id,
            price=base_price,
            seat_number="A1",
            ticket_type="Standard",
            purchase_date="2025-01-01",
            is_used=False
        )

        self.assertAlmostEqual(ticket.price, 100.0)
        self.assertEqual(ticket.ticket_type, "Standard")

    def test_vip_pricing(self):
        """
        VipPricing: final price = base price * 1.5
        """
        base_price = 100.0
        ticket = self.ticket_service.sell_ticket(
            event_id=self.event_id,
            participant_id=self.participant_id,
            price=base_price,
            seat_number="B2",
            ticket_type="VIP",
            purchase_date="2025-01-01",
            is_used=False
        )

        self.assertAlmostEqual(ticket.price, 150.0)
        self.assertEqual(ticket.ticket_type, "VIP")

    def test_student_pricing(self):
        """
        StudentPricing: final price = base price * 0.7
        """
        base_price = 100.0
        ticket = self.ticket_service.sell_ticket(
            event_id=self.event_id,
            participant_id=self.participant_id,
            price=base_price,
            seat_number="C3",
            ticket_type="Student",
            purchase_date="2025-01-01",
            is_used=False
        )

        self.assertAlmostEqual(ticket.price, 70.0)
        self.assertEqual(ticket.ticket_type, "Student")

    def test_sell_ticket_negative_price_raises(self):
        """
        Mənfi qiymət gələndə error atmalıdır.
        """
        with self.assertRaises(ValueError):
            self.ticket_service.sell_ticket(
                event_id=self.event_id,
                participant_id=self.participant_id,
                price=-10.0,
                seat_number="D4",
                ticket_type="Standard",
                purchase_date="2025-01-01",
                is_used=False
            )

    def test_update_and_delete_ticket(self):
        """
        Update + delete CRUD əməliyyatlarının işlədiyini yoxlayır.
        """
        ticket = self.ticket_service.sell_ticket(
            event_id=self.event_id,
            participant_id=self.participant_id,
            price=50.0,
            seat_number="E5",
            ticket_type="Standard",
            purchase_date="2025-01-01",
            is_used=False
        )

        # UPDATE
        updated = self.ticket_service.update_ticket(
            ticket_id=ticket.id,
            event_id=ticket.event_id,
            participant_id=ticket.participant_id,
            price=60.0,
            seat_number="E6",
            ticket_type="VIP",
            purchase_date="2025-01-02",
            is_used=True
        )

        self.assertEqual(updated.price, 60.0)
        self.assertEqual(updated.seat_number, "E6")
        self.assertEqual(updated.ticket_type, "VIP")
        self.assertTrue(updated.is_used)

        # DELETE
        deleted = self.ticket_service.delete_ticket(ticket.id)
        self.assertTrue(deleted)


if __name__ == "__main__":
    unittest.main()
