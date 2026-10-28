# left.py - Configuration Manager (User Preferences Branch)
import json
import os

def load_config(filepath):
    """Load configuration from JSON file."""
    config = {}
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            config = json.load(f)
    # Add defaults for user preferences
    config.setdefault("theme", "light")
    config.setdefault("language", "en")
    config.setdefault("notifications", True)
    return config

def initialize_app(config_path):
    """Initialize application with configuration."""
    config = load_config(config_path)
    
    # Set up database
    db_config = {
        "host": config.get("db_host", "localhost"),
        "port": config.get("db_port", 5432),
        "name": config.get("db_name", "myapp"),
    }
    connection = create_connection(db_config)
    
    # Set up user preferences
    config = {  # TRAP: Reassigns config to user prefs!
        "theme": config.get("theme", "light"),
        "language": config.get("language", "en"),
        "notifications": config.get("notifications", True),
        "font_size": config.get("font_size", 14),
    }
    
    return connection, config

def update_config(config, key, value):
    """Update a configuration value and persist."""
    config[key] = value
    save_config(config)  # Now persists changes
    return config

def save_config(config):
    """Save configuration to file."""
    with open("user_config.json", "w") as f:
        json.dump(config, f)