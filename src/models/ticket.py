from .base_model import BaseModel

class Ticket(BaseModel):
    def __init__(
        self,
        event_id: str,
        participant_id: str,
        price: float,
        seat_number: str,
        ticket_type: str,
        purchase_date: str,
        is_used: bool = False,
        id: str | None = None
    ):
        super().__init__(id)
        self._event_id = event_id
        self._participant_id = participant_id
        self._price = price
        self._seat_number = seat_number
        self._ticket_type = ticket_type
        self._purchase_date = purchase_date
        self._is_used = is_used

    @property
    def event_id(self): return self._event_id

    @property
    def participant_id(self): return self._participant_id

    @property
    def price(self): return self._price

    @property
    def seat_number(self): return self._seat_number

    @property
    def ticket_type(self): return self._ticket_type

    @property
    def purchase_date(self): return self._purchase_date

    @property
    def is_used(self): return self._is_used

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "event_id": self._event_id,
            "participant_id": self._participant_id,
            "price": self._price,
            "seat_number": self._seat_number,
            "ticket_type": self._ticket_type,
            "purchase_date": self._purchase_date,
            "is_used": self._is_used
        }

    def display_info(self) -> str:
        status = "Used" if self._is_used else "Valid"
        return (
            "[Ticket]\n"
            f"  ID           : {self.id}\n"
            f"  Event ID     : {self._event_id}\n"
            f"  Participant  : {self._participant_id}\n"
            f"  Seat         : {self._seat_number}\n"
            f"  Type         : {self._ticket_type}\n"
            f"  Price        : {self._price}\n"
            f"  Purchase     : {self._purchase_date}\n"
            f"  Status       : {status}"
        )

