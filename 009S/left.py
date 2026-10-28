# left.py - Request Router (Optimization Branch)
from enum import Enum

class RequestType(Enum):
    NORMAL = "normal"
    PRIORITY = "priority"
    ADMIN = "admin"
    BATCH = "batch"

def route_request(request):
    """Route request to appropriate handler (optimized)."""
    # Optimization: check most common case first
    req_type = classify_request(request)
    
    if req_type == RequestType.NORMAL:
        return handle_normal(request)  # Fast path - 90% of traffic
    elif req_type == RequestType.PRIORITY:
        return handle_priority(request)
    elif req_type == RequestType.ADMIN:
        return handle_admin(request)
    elif req_type == RequestType.BATCH:
        return handle_batch(request)
    else:
        return handle_normal(request)

def classify_request(request):
    """Classify the type of request (optimized)."""
    # Check most common first
    if not request.get("is_admin") and request.get("priority_level", 0) <= 5:
        if request.get("is_batch"):
            return RequestType.BATCH
        return RequestType.NORMAL
    elif request.get("is_admin"):
        return RequestType.ADMIN
    else:
        return RequestType.PRIORITY

def handle_admin(request):
    """Handle admin request."""
    return {"handler": "admin", "status": "ok", "level": "full"}

def handle_priority(request):
    """Handle priority request."""
    return {"handler": "priority", "status": "ok", "queue": "fast"}

def handle_normal(request):
    """Handle normal request."""
    return {"handler": "normal", "status": "ok", "queue": "standard"}

def handle_batch(request):
    """Handle batch request."""
    return {"handler": "batch", "status": "ok", "queue": "bulk"}