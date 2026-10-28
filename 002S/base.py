# base.py - Pricing Module
from decimal import Decimal, ROUND_HALF_UP

TAX_RATE = Decimal("0.08")

def calculate_price(base_price, quantity):
    """Calculate total price with tax."""
    subtotal = base_price * quantity
    tax = subtotal * TAX_RATE
    total = subtotal + tax
    return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def apply_discount(price, discount_percent):
    """Apply a percentage discount to price."""
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be between 0 and 100")
    discount = price * Decimal(str(discount_percent)) / Decimal("100")
    return (price - discount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def get_final_price(base_price, quantity, discount_percent=0):
    """Get final price after discount and tax."""
    subtotal = base_price * quantity
    discounted = apply_discount(subtotal, discount_percent)
    tax = discounted * TAX_RATE
    return (discounted + tax).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)