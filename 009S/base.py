# base.py - Request Router
from enum import Enum

class RequestType(Enum):
    NORMAL = "normal"
    PRIORITY = "priority"
    ADMIN = "admin"

def route_request(request):
    """Route request to appropriate handler."""
    req_type = classify_request(request)
    
    if req_type == RequestType.ADMIN:
        return handle_admin(request)
    elif req_type == RequestType.PRIORITY:
        return handle_priority(request)
    else:
        return handle_normal(request)

def classify_request(request):
    """Classify the type of request."""
    if request.get("is_admin"):
        return RequestType.ADMIN
    elif request.get("priority_level", 0) > 5:
        return RequestType.PRIORITY
    return RequestType.NORMAL

def handle_admin(request):
    """Handle admin request."""
    return {"handler": "admin", "status": "ok"}

def handle_priority(request):
    """Handle priority request."""
    return {"handler": "priority", "status": "ok"}

def handle_normal(request):
    """Handle normal request."""
    return {"handler": "normal", "status": "ok"}