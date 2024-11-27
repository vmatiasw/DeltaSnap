import os
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

PASSWORD = "test_password"
USERNAME = "test_user"
DATABASE_NAME = "test_db"
DATABASE_PATH = os.path.join(os.path.dirname(__file__), "test.db")

# SQLite
# URL_DATABASE = f"sqlite:///{DATABASE_PATH}"
# MySQL: sudo systemctl start mysql
URL_DATABASE = f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@localhost/{DATABASE_NAME}"
# PostgreSQL: sudo systemctl start postgresql
# URL_DATABASE = f"postgresql://{USERNAME}:{PASSWORD}@localhost/{DATABASE_NAME}"

engine = create_engine(URL_DATABASE)

localSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass
