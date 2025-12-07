from .pricing_strategy import PricingStrategy


class VipPricing(PricingStrategy):
    """
    VIP ticket pricing:
    Final price = base price * 1.5 (50% more).
    """

    def calculate_price(self, base_price: float) -> float:
        return base_price * 1.5
