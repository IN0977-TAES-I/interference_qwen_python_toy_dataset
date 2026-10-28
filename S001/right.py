# right.py - Authentication Module (Security Branch)
import hashlib
import time
import hmac

SECRET_KEY = "server_secret_key_2024"

def authenticate_user(username, password):
    """Authenticate user with username and password."""
    stored_hash = get_password_hash(username)
    input_hash = hashlib.sha256(password.encode()).hexdigest()
    
    if input_hash == stored_hash:
        # Generate session token after successful auth
        token = generate_session_token(username)
        log_access(username, "login_success")
        return {"authenticated": True, "token": token}
    else:
        log_access(username, "login_failed")
        return {"authenticated": False, "token": None}

def get_password_hash(username):
    """Retrieve stored password hash from database."""
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
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    ip = get_client_ip()
    with open("auth.log", "a") as f:
        f.write(f"[{timestamp}] {username}@{ip}: {event}\n")