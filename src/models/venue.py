from .base_model import BaseModel

class Venue(BaseModel):
    def __init__(
        self,
        name: str,
        address: str,
        capacity: int,
        manager_name: str,
        phone: str,
        is_open: bool = True,
        id: str | None = None
    ):
        super().__init__(id)
        self._name = name
        self._address = address
        self._capacity = capacity
        self._manager_name = manager_name
        self._phone = phone
        self._is_open = is_open

    @property
    def name(self): return self._name

    @property
    def address(self): return self._address

    @property
    def capacity(self): return self._capacity

    @property
    def manager_name(self): return self._manager_name

    @property
    def phone(self): return self._phone

    @property
    def is_open(self): return self._is_open

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self._name,
            "address": self._address,
            "capacity": self._capacity,
            "manager_name": self._manager_name,
            "phone": self._phone,
            "is_open": self._is_open
        }

    def display_info(self) -> str:
        status = "Open" if self._is_open else "Closed"
        return (
            "[Venue]\n"
            f"  ID         : {self.id}\n"
            f"  Name       : {self._name}\n"
            f"  Address    : {self._address}\n"
            f"  Capacity   : {self._capacity}\n"
            f"  Manager    : {self._manager_name}\n"
            f"  Phone      : {self._phone}\n"
            f"  Status     : {status}"
        )

