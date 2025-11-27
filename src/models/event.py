from .base_model import BaseModel

class Event(BaseModel):
    def __init__(
        self,
        name: str,
        date: str,
        time: str,
        category: str,
        description: str,
        duration_minutes: int,
        venue_id: str,
        is_active: bool = True,
        id: str | None = None
    ):
        super().__init__(id)
        self._name = name
        self._date = date
        self._time = time
        self._category = category
        self._description = description
        self._duration_minutes = duration_minutes
        self._venue_id = venue_id
        self._is_active = is_active

    @property
    def name(self): return self._name

    @property
    def date(self): return self._date

    @property
    def time(self): return self._time

    @property
    def category(self): return self._category

    @property
    def description(self): return self._description

    @property
    def duration_minutes(self): return self._duration_minutes

    @property
    def venue_id(self): return self._venue_id

    @property
    def is_active(self): return self._is_active

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self._name,
            "date": self._date,
            "time": self._time,
            "category": self._category,
            "description": self._description,
            "duration_minutes": self._duration_minutes,
            "venue_id": self._venue_id,
            "is_active": self._is_active
        }

    def display_info(self) -> str:
        status = "Active" if self._is_active else "Canceled"
        return (
            "[Event]\n"
            f"  ID          : {self.id}\n"
            f"  Name        : {self._name}\n"
            f"  Category    : {self._category}\n"
            f"  Date & Time : {self._date} {self._time}\n"
            f"  Duration    : {self._duration_minutes} min\n"
            f"  Venue ID    : {self._venue_id}\n"
            f"  Status      : {status}"
        )
    
