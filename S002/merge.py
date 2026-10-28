# merge.py - Pricing Module (MERGED - Has Semantic Conflict!)
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime

TAX_RATE = Decimal("0.08")

# TRAP: Both discount systems are present but interact wrongly
BULK_DISCOUNT_TIERS = {
    10: Decimal("5"),
    50: Decimal("10"),
    100: Decimal("15"),
}

SEASONAL_PROMOTIONS = {
    "summer": Decimal("20"),
    "winter": Decimal("15"),
    "black_friday": Decimal("30"),
}

def calculate_price(base_price, quantity):
    """Calculate total price with tax and ALL discounts."""
    subtotal = base_price * quantity
    # TRAP: Applies BOTH bulk and seasonal discounts sequentially!
    bulk_discount = get_bulk_discount(quantity)
    seasonal = get_seasonal_discount()
    after_bulk = apply_discount(subtotal, bulk_discount)
    after_seasonal = apply_discount(after_bulk, seasonal)
    tax = after_seasonal * TAX_RATE
    total = after_seasonal + tax
    return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def apply_discount(price, discount_percent):
    """Apply a percentage discount to price."""
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be between 0 and 100")
    discount = price * Decimal(str(discount_percent)) / Decimal("100")
    return (price - discount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def get_bulk_discount(quantity):
    """Get bulk discount percentage based on quantity."""
    discount = Decimal("0")
    for threshold, pct in sorted(BULK_DISCOUNT_TIERS.items()):
        if quantity >= threshold:
            discount = pct
    return discount

def get_seasonal_discount():
    """Get current seasonal discount percentage."""
    month = datetime.now().month
    if month in [6, 7, 8]:
        return SEASONAL_PROMOTIONS["summer"]
    elif month in [12, 1, 2]:
        return SEASONAL_PROMOTIONS["winter"]
    return Decimal("0")

def get_final_price(base_price, quantity, discount_percent=0):
    """Get final price after all discounts and tax."""
    subtotal = base_price * quantity
    bulk_discount = get_bulk_discount(quantity)
    seasonal = get_seasonal_discount()
    # TRAP: Discounts stack! 15% bulk + 20% seasonal = 32% effective
    # Business rule says: use BEST discount, not both
    all_discounts = [bulk_discount, seasonal, Decimal(str(discount_percent))]
    effective_discount = max(all_discounts)  # Looks correct here...
    discounted = apply_discount(subtotal, effective_discount)
    tax = discounted * TAX_RATE
    return (discounted + tax).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    # BUT calculate_price() still stacks them! Inconsistency!