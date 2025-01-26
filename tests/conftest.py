import os

os.environ["TESTING"] = "1"

import pytest
from sqlmodel import Session, create_engine, SQLModel
from fastapi.testclient import TestClient

import app.models  # Ensure models are imported
from app.main import app
from app.database import get_session

# Reuse the same shared in-memory DB
TEST_DATABASE_URL = "sqlite:///file::memory:?cache=shared"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False, "uri": True},
    echo=False,
)


def override_get_session():
    with Session(test_engine) as session:
        yield session


@pytest.fixture(scope="function", autouse=True)
def fresh_db():
    """
    Function-scoped fixture that starts each test with an empty DB.
    """
    # Drop + re-create tables
    SQLModel.metadata.drop_all(test_engine)
    SQLModel.metadata.create_all(test_engine)
    yield
    # (Optional) drop again if you want to ensure absolutely clean for next test
    # SQLModel.metadata.drop_all(test_engine)


@pytest.fixture
def client():
    app.dependency_overrides[get_session] = override_get_session
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def db_session():
    """
    Provides a database session without any pre-inserted data.
    """
    with Session(test_engine) as session:
        yield session


@pytest.fixture
def prepopulated_db_session():
    """
    Provides a database session pre-populated with initial data.
    """
    with Session(test_engine) as session:
        from app.models import Product

        # Insert a product so we can test orders
        product = Product(name="Widget", description="A widget", price=10.0, stock=5)
        session.add(product)
        session.commit()
        session.refresh(product)
        yield session
