from abc import ABC

class BaseService(ABC):
    """
    Common base class for all services.
    Holds a reference to the corresponding repository.
    """
    def __init__(self, repository):
        self._repository = repository

    @property
    def repository(self):
        return self._repository
