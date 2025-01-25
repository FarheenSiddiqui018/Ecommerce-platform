import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session

# 1. Load environment variables from .env
load_dotenv()

# 2. Retrieve the environment variables
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "test_db")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

engine = create_engine(DATABASE_URL, echo=False)

def get_session():
    """
    Get a new database session.
    """
    with Session(engine) as session:
        yield session

def init_db():
    """
    Create all tables. This can be run on startup to ensure tables exist.
    """
    SQLModel.metadata.create_all(engine)
