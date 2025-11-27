from .base_model import BaseModel

class Participant(BaseModel):
    def __init__(
        self,
        full_name: str,
        email: str,
        phone: str,
        age: int,
        gender: str,
        registration_date: str,
        is_vip: bool = False,
        id: str | None = None
    ):
        super().__init__(id)
        self._full_name = full_name
        self._email = email
        self._phone = phone
        self._age = age
        self._gender = gender
        self._registration_date = registration_date
        self._is_vip = is_vip

    @property
    def full_name(self): return self._full_name

    @property
    def email(self): return self._email

    @property
    def phone(self): return self._phone

    @property
    def age(self): return self._age

    @property
    def gender(self): return self._gender

    @property
    def registration_date(self): return self._registration_date

    @property
    def is_vip(self): return self._is_vip

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "full_name": self._full_name,
            "email": self._email,
            "phone": self._phone,
            "age": self._age,
            "gender": self._gender,
            "registration_date": self._registration_date,
            "is_vip": self._is_vip
        }

    def display_info(self) -> str:
        vip = "VIP" if self._is_vip else "Standard"
        return (
            "[Participant]\n"
            f"  ID          : {self.id}\n"
            f"  Name        : {self._full_name}\n"
            f"  Email       : {self._email}\n"
            f"  Phone       : {self._phone}\n"
            f"  Age         : {self._age}\n"
            f"  Gender      : {self._gender}\n"
            f"  Reg. Date   : {self._registration_date}\n"
            f"  Type        : {vip}"
        )

