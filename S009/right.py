# right.py - Request Router (Security Branch)
from enum import Enum

class RequestType(Enum):
    NORMAL = "normal"
    PRIORITY = "priority"
    ADMIN = "admin"
    SUSPICIOUS = "suspicious"

def route_request(request):
    """Route request to appropriate handler (security-first)."""
    req_type = classify_request(request)
    
    # Security: check suspicious FIRST
    if req_type == RequestType.SUSPICIOUS:
        return handle_suspicious(request)
    elif req_type == RequestType.ADMIN:
        return handle_admin(request)
    elif req_type == RequestType.PRIORITY:
        return handle_priority(request)
    else:
        return handle_normal(request)

def classify_request(request):
    """Classify the type of request (with security checks)."""
    # Security check first
    if is_suspicious(request):
        return RequestType.SUSPICIOUS
    if request.get("is_admin"):
        return RequestType.ADMIN
    elif request.get("priority_level", 0) > 5:
        return RequestType.PRIORITY
    return RequestType.NORMAL

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
    return {"handler": "admin", "status": "ok"}

def handle_priority(request):
    """Handle priority request."""
    return {"handler": "priority", "status": "ok"}

def handle_normal(request):
    """Handle normal request."""
    return {"handler": "normal", "status": "ok"}

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