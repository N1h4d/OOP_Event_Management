from abc import ABC, abstractmethod
import uuid

class BaseModel(ABC):
    """
    Abstraction + Encapsulation
    """
    def __init__(self, id: str | None = None):
        self._id = id or str(uuid.uuid4())

    @property
    def id(self) -> str:
        return self._id

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @abstractmethod
    def display_info(self) -> str:
        pass
