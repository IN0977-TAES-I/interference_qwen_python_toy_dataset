# right.py - Order Processing Module (Flexible Response Branch)
from datetime import datetime

def process_order(order_id, items, customer):
    """Process an order and return detailed result dict."""
    total = sum(item["price"] * item["qty"] for item in items)
    tax = total * 0.08
    grand_total = total + tax
    
    for item in items:
        stock = get_inventory(item["id"])
        if stock < item["qty"]:
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
    
    return {
        "status": "success",
        "order": order,
        "estimated_delivery": calculate_delivery(customer),
    }

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