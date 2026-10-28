# left.py - Order Processing Module (Type Safety Branch)
from datetime import datetime
from typing import NamedTuple, List, Optional
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
    
    for item in items:
        if not check_stock(item["id"], item["qty"]):
            return OrderResult(status="failed", reason="out_of_stock")
    
    order = {
        "id": order_id,
        "items": items,
        "total": total,
        "customer": customer,
        "timestamp": datetime.now().isoformat(),
    }
    
    save_order(order)
    send_confirmation(customer["email"], order)
    
    return OrderResult(status="success", order_id=order_id, total=total)

def check_stock(item_id, quantity):
    """Check if item is in stock."""
    inventory = get_inventory(item_id)
    return inventory >= quantity

def save_order(order):
    """Save order to database."""
    db = get_database()
    db.insert("orders", order)

def send_confirmation(email, order):
    """Send order confirmation email."""
    template = load_email_template("confirmation")
    body = template.format(order_id=order["id"], total=order["total"])
    send_email(email, "Order Confirmation", body)