# base.py - Authentication Module
import hashlib
import time

def authenticate_user(username, password):
    """Authenticate user with username and password."""
    stored_hash = get_password_hash(username)
    input_hash = hashlib.sha256(password.encode()).hexdigest()
    
    if input_hash == stored_hash:
        log_access(username, "login_success")
        return True
    else:
        log_access(username, "login_failed")
        return False

def get_password_hash(username):
    """Retrieve stored password hash from database."""
    db = get_database_connection()
    result = db.execute(
        "SELECT password_hash FROM users WHERE username = ?",
        (username,)
    )
    return result.fetchone()[0]

def check_access(user_role, required_permission):
    """Check if user has required permission."""
    permissions = get_role_permissions(user_role)
    if required_permission in permissions:
        return True
    return False

def log_access(username, event):
    """Log authentication events."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open("auth.log", "a") as f:
        f.write(f"[{timestamp}] {username}: {event}\n")