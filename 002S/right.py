# right.py - Pricing Module (Seasonal Discount Branch)
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime

TAX_RATE = Decimal("0.08")

# Seasonal promotions
SEASONAL_PROMOTIONS = {
    "summer": Decimal("20"),    # 20% off in summer
    "winter": Decimal("15"),    # 15% off in winter
    "black_friday": Decimal("30"),  # 30% off on black friday
}

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

def get_seasonal_discount():
    """Get current seasonal discount percentage."""
    month = datetime.now().month
    if month in [6, 7, 8]:
        return SEASONAL_PROMOTIONS["summer"]
    elif month in [12, 1, 2]:
        return SEASONAL_PROMOTIONS["winter"]
    return Decimal("0")

def get_final_price(base_price, quantity, discount_percent=0):
    """Get final price after seasonal discount and tax."""
    subtotal = base_price * quantity
    seasonal = get_seasonal_discount()
    # Use the better discount
    effective_discount = max(seasonal, Decimal(str(discount_percent)))
    discounted = apply_discount(subtotal, effective_discount)
    tax = discounted * TAX_RATE
    return (discounted + tax).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)