# base.py - Order Processing Module
from datetime import datetime

def process_order(order_id, items, customer):
    """Process an order and return result."""
    total = sum(item["price"] * item["qty"] for item in items)
    
    # Validate stock
    for item in items:
        if not check_stock(item["id"], item["qty"]):
            return {"status": "failed", "reason": "out_of_stock"}
    
    # Create order record
    order = {
        "id": order_id,
        "items": items,
        "total": total,
        "customer": customer,
        "timestamp": datetime.now().isoformat(),
    }
    
    save_order(order)
    send_confirmation(customer["email"], order)
    
    return {"status": "success", "order": order}

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