# merge.py - Request Router (MERGED - Has Semantic Conflict!)
from enum import Enum

class RequestType(Enum):
    NORMAL = "normal"
    PRIORITY = "priority"
    ADMIN = "admin"
    BATCH = "batch"
    SUSPICIOUS = "suspicious"

def route_request(request):
    """Route request to appropriate handler."""
    req_type = classify_request(request)
    
    # TRAP: Security check first (from right) catches priority
    # batch requests as suspicious before batch handler can run!
    if req_type == RequestType.SUSPICIOUS:
        return handle_suspicious(request)
    elif req_type == RequestType.NORMAL:
        return handle_normal(request)  # Left's optimization
    elif req_type == RequestType.PRIORITY:
        return handle_priority(request)
    elif req_type == RequestType.ADMIN:
        return handle_admin(request)
    elif req_type == RequestType.BATCH:
        return handle_batch(request)
    else:
        return handle_normal(request)

def classify_request(request):
    """Classify the type of request."""
    # TRAP: is_suspicious() check runs FIRST and may classify
    # legitimate batch requests as suspicious!
    if is_suspicious(request):
        return RequestType.SUSPICIOUS
    # TRAP: Left's optimization logic conflicts with right's order
    if not request.get("is_admin") and request.get("priority_level", 0) <= 5:
        if request.get("is_batch"):
            return RequestType.BATCH
        return RequestType.NORMAL
    elif request.get("is_admin"):
        return RequestType.ADMIN
    else:
        return RequestType.PRIORITY

def is_suspicious(request):
    """Check if request looks suspicious."""
    suspicious_patterns = [
        request.get("ip", "") in get_blocked_ips(),
        request.get("rate_exceeded", False),
        request.get("malformed_headers", False),
    ]
    return any(suspicious_patterns)

def get_blocked_ips():
    """Get list of blocked IPs."""
    return {"192.168.1.100", "10.0.0.50"}

def handle_admin(request):
    """Handle admin request with extra verification."""
    if not verify_admin_token(request):
        return {"handler": "admin", "status": "denied"}
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

def handle_suspicious(request):
    """Handle suspicious request."""
    log_security_event(request)
    return {"handler": "suspicious", "status": "blocked"}

def verify_admin_token(request):
    """Verify admin authentication token."""
    return request.get("admin_token") == "valid_token"

def log_security_event(request):
    """Log security event."""
    pass

# TRAP SCENARIO:
# Batch requests from IP 192.168.1.100 (internal CI server)
# are classified as SUSPICIOUS and blocked!
# The batch handler is never reached for these requests.
# is_suspicious() runs before is_batch check, so legitimate
# batch traffic from known IPs gets blocked.