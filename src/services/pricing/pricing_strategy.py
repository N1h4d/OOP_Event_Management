from abc import ABC, abstractmethod


class PricingStrategy(ABC):
    """
    Strategy interface for ticket pricing.
    Different implementations can provide
    different pricing rules (Standard, VIP, Student, etc.).
    """

    @abstractmethod
    def calculate_price(self, base_price: float) -> float:
        pass
