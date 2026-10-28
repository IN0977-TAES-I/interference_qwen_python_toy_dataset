# left.py - Pricing Module (Bulk Discount Branch)
from decimal import Decimal, ROUND_HALF_UP

TAX_RATE = Decimal("0.08")

# Bulk discount tiers
BULK_DISCOUNT_TIERS = {
    10: Decimal("5"),   # 5% off for 10+ items
    50: Decimal("10"),  # 10% off for 50+ items
    100: Decimal("15"), # 15% off for 100+ items
}

def calculate_price(base_price, quantity):
    """Calculate total price with tax and bulk discount."""
    subtotal = base_price * quantity
    bulk_discount = get_bulk_discount(quantity)
    discounted = apply_discount(subtotal, bulk_discount)
    tax = discounted * TAX_RATE
    total = discounted + tax
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

def get_final_price(base_price, quantity, discount_percent=0):
    """Get final price after bulk discount and tax."""
    subtotal = base_price * quantity
    bulk_discount = get_bulk_discount(quantity)
    # Use the better discount
    effective_discount = max(bulk_discount, Decimal(str(discount_percent)))
    discounted = apply_discount(subtotal, effective_discount)
    tax = discounted * TAX_RATE
    return (discounted + tax).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)