# merge.py - Order Processing Module (MERGED - Has Semantic Conflict!)
from datetime import datetime
from typing import NamedTuple, Optional
from dataclasses import dataclass

@dataclass
class OrderResult:
    status: str
    order_id: Optional[str] = None
    total: Optional[float] = None
    reason: Optional[str] = None

def process_order(order_id, items, customer) -> OrderResult:
    """Process an order and return typed result."""
    total = sum(item["price"] * item["qty"] for item in items)
    tax = total * 0.08
    grand_total = total + tax
    
    for item in items:
        stock = get_inventory(item["id"])
        if stock < item["qty"]:
            # TRAP: Returns dict here but function signature says OrderResult!
            return {
                "status": "failed",
                "reason": "insufficient_stock",
                "item_id": item["id"],
                "available": stock,
                "requested": item["qty"],
            }
    
    order = {
        "id": order_id,
        "items": items,
        "subtotal": total,
        "tax": tax,
        "total": grand_total,
        "customer": customer,
        "timestamp": datetime.now().isoformat(),
    }
    
    save_order(order)
    send_confirmation(customer["email"], order)
    
    # TRAP: Returns OrderResult but loses order details!
    # Caller can't access order["subtotal"], order["tax"], etc.
    return OrderResult(status="success", order_id=order_id, total=grand_total)

def check_stock(item_id, quantity):
    """Check if item is in stock."""
    inventory = get_inventory(item_id)
    return inventory >= quantity

def calculate_delivery(customer):
    """Calculate estimated delivery date."""
    from datetime import timedelta
    base_days = 5
    if customer.get("premium"):
        base_days = 2
    return (datetime.now() + timedelta(days=base_days)).isoformat()

def save_order(order):
    """Save order to database with tax info."""
    db = get_database()
    db.insert("orders", order)

def send_confirmation(email, order):
    """Send order confirmation email with tax breakdown."""
    template = load_email_template("confirmation_v2")
    body = template.format(
        order_id=order["id"],
        subtotal=order["subtotal"],
        tax=order["tax"],
        total=order["total"],
    )
    send_email(email, "Order Confirmation", body)

# TRAP: Usage example showing the problem:
# result = process_order(1, items, customer)
# if result["status"] == "failed":  # Works for failure path
#     print(result["item_id"])       # Works for failure path
# else:
#     print(result.order_id)         # Works for success path
#     print(result["total"])         # CRASH! OrderResult has no [] access!