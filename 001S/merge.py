# merge.py - Authentication Module (MERGED - Has Semantic Conflict!)
import hashlib
import time
import hmac
import os

# TRAP: is_testing from left branch is kept
is_testing = os.environ.get("TESTING", "false") == "true"
SECRET_KEY = "server_secret_key_2024"

def authenticate_user(username, password):
    """Authenticate user with username and password."""
    # TRAP: Testing bypass from left remains!
    if is_testing:
        return True  # Returns bool, but right branch expects dict!
    
    stored_hash = get_password_hash(username)
    input_hash = hashlib.sha256(password.encode()).hexdigest()
    
    if input_hash == stored_hash:
        token = generate_session_token(username)
        log_access(username, "login_success")
        # TRAP: Inconsistent return - True vs dict
        return {"authenticated": True, "token": token}
    else:
        log_access(username, "login_failed")
        return {"authenticated": False, "token": None}

def get_password_hash(username):
    """Retrieve stored password hash from database."""
    # TRAP: Testing shortcut bypasses error handling
    if is_testing:
        return "test_hash_placeholder"
    db = get_database_connection()
    result = db.execute(
        "SELECT password_hash FROM users WHERE username = ?",
        (username,)
    )
    row = result.fetchone()
    if row is None:
        raise UserNotFoundError(f"User {username} not found")
    return row[0]

def check_access(user_role, required_permission):
    """Check if user has required permission with audit trail."""
    # TRAP: Testing bypass skips audit trail!
    if is_testing:
        return True
    permissions = get_role_permissions(user_role)
    has_access = required_permission in permissions
    audit_log(user_role, required_permission, has_access)
    return has_access

def verify_token(token):
    """Verify session token integrity."""
    if not token:
        return False
    parts = token.split(".")
    if len(parts) != 2:
        return False
    payload, signature = parts
    expected = hmac.new(
        SECRET_KEY.encode(), payload.encode(), hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)

def log_access(username, event):
    """Log authentication events with enhanced detail."""
    # TRAP: Testing flag disables ALL logging including security events
    if is_testing:
        return
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    ip = get_client_ip()
    with open("auth.log", "a") as f:
        f.write(f"[{timestamp}] {username}@{ip}: {event}\n")