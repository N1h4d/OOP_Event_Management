from .pricing_strategy import PricingStrategy


class StudentPricing(PricingStrategy):
    """
    Student ticket pricing:
    Final price = base price * 0.7 (30% discount).
    """

    def calculate_price(self, base_price: float) -> float:
        return base_price * 0.7
