from .pricing_strategy import PricingStrategy


class StandardPricing(PricingStrategy):
    """
    Standard ticket pricing:
    Final price = base price (no change).
    """

    def calculate_price(self, base_price: float) -> float:
        return base_price
