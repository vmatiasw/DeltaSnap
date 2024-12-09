import os

# This file is used to configure the database connection for the tests

# List of available ORMs/DBs
DB_SOURCES = ["sqlalchemy", "django"]

# Database configuration
HOST = "localhost"
PORT = ""
PASSWORD = "test_password"
USERNAME = "test_user"
DATABASE = "sqlite"  # sqlite | mysql | postgresql
DATABASE_NAME = "test_db"

DB_PATH = os.path.join(f"tests/db/connection/{DATABASE_NAME}.db")

APP_LABEL = "__main__"  # "test_app"
