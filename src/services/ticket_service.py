# src/services/ticket_service.py

from typing import List

from ..models.ticket import Ticket
from ..repositories.ticket_repository import TicketRepository
from ..logging_config import get_logger
from .base_service import BaseService

from .pricing.pricing_strategy import PricingStrategy
from .pricing.standard_pricing import StandardPricing
from .pricing.vip_pricing import VipPricing
from .pricing.student_pricing import StudentPricing

logger = get_logger(__name__)


class TicketService(BaseService):
    def __init__(self, repository: TicketRepository):
        super().__init__(repository)

    # ---------- Strategy seçimi ---------- #

    def _get_pricing_strategy(self, ticket_type: str) -> PricingStrategy:
        """
        Selects a pricing strategy based on ticket_type string.
        """
        t = (ticket_type or "").strip().lower()
        if t == "vip":
            return VipPricing()
        elif t == "student":
            return StudentPricing()
        else:
            # default: Standard
            return StandardPricing()

    # ---------- Create / Sell Ticket ---------- #

    def sell_ticket(
        self,
        event_id: str,
        participant_id: str,
        price: float,          # base price
        seat_number: str,
        ticket_type: str,
        purchase_date: str,
        is_used: bool = False
    ) -> Ticket:
        """
        Creates and saves a ticket using the Strategy pattern
        to calculate the final price based on ticket type.
        """
        if price < 0:
            raise ValueError("Price cannot be negative.")

        strategy = self._get_pricing_strategy(ticket_type)
        final_price = strategy.calculate_price(price)

        ticket = Ticket(
            event_id=event_id,
            participant_id=participant_id,
            price=final_price,
            seat_number=seat_number,
            ticket_type=ticket_type,
            purchase_date=purchase_date,
            is_used=is_used
        )

        self.repository.add(ticket)

        # ✅ sadə, biznes səviyyəli log
        logger.info(
            "Ticket sold: id=%s, type=%s, base_price=%.2f, final_price=%.2f",
            ticket.id,
            ticket.ticket_type,
            price,
            final_price,
        )

        return ticket

    # ---------- Read ---------- #

    def list_tickets(self) -> List[Ticket]:
        tickets = self.repository.get_all()
        # istəsən bu logu saxla, istəsən sil – zəruri deyil, amma pis də deyil
        logger.info("Retrieved %d tickets.", len(tickets))
        return tickets

    # ---------- Update ---------- #

    def update_ticket(
        self,
        ticket_id: str,
        event_id: str,
        participant_id: str,
        price: float,
        seat_number: str,
        ticket_type: str,
        purchase_date: str,
        is_used: bool
    ) -> Ticket:
        """
        Updates ticket fields. Here we assume 'price' is already
        the final price (we don't reapply strategy on update),
        but we could if needed.
        """
        ticket = self.repository.get_by_id(ticket_id)
        if ticket is None:
            raise ValueError("Ticket not found.")

        if price < 0:
            raise ValueError("Price cannot be negative.")

        ticket._event_id = event_id
        ticket._participant_id = participant_id
        ticket._price = price
        ticket._seat_number = seat_number
        ticket._ticket_type = ticket_type
        ticket._purchase_date = purchase_date
        ticket._is_used = is_used

        self.repository.update(ticket)

        # ✅ update log
        logger.info(
            "Ticket updated: id=%s, type=%s, price=%.2f",
            ticket.id,
            ticket.ticket_type,
            ticket.price,
        )

        return ticket

    # ---------- Delete ---------- #

    def delete_ticket(self, ticket_id: str) -> bool:
        deleted = self.repository.delete_by_id(ticket_id)
        if not deleted:
            raise ValueError("Ticket not found.")

        # ✅ delete log
        logger.info("Ticket deleted: id=%s", ticket_id)

        return True
