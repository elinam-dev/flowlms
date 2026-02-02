# Configuration settings for the backend

# Database settings
database = {
    "host": "localhost",
    "port": 5432,
    "user": "admin",
    "password": "password",
    "database": "flowlms_db"
}

# Application settings
app_settings = {
    "debug": True,
    "secret_key": "your_secret_key",
    "allowed_hosts": ["localhost", "127.0.0.1"]
}

# Logging settings
logging = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}