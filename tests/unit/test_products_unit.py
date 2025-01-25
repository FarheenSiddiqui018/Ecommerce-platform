# tests/unit/test_products_unit.py

import pytest
from sqlmodel import Session, select
from fastapi import HTTPException

from app.models import Product
from app.schemas import ProductCreate
from app.services.product_service import create_product

@pytest.fixture
def db_session():
    """
    This fixture creates a session on the shared in-memory test DB (test_engine).
    Yields the session for each test.
    """
    from tests.conftest import test_engine  # import the shared test engine here
    with Session(test_engine) as session:
        yield session

def test_create_product_positive(db_session):
    """
    Test that creating a product with valid data succeeds.
    """
    product_data = ProductCreate(
        name="Test Product",
        description="Test Description",
        price=10.50,
        stock=100
    )
    product = create_product(db_session, product_data)
    assert product.id is not None
    assert product.name == "Test Product"
    assert product.stock == 100

def test_create_product_negative_price(db_session):
    """
    Test that creating a product with a negative price raises an exception.
    """
    product_data = ProductCreate(
        name="Test Negative Price",
        description="Testing negative price",
        price=-5.00,
        stock=10
    )
    with pytest.raises(HTTPException) as exc_info:
        create_product(db_session, product_data)
    assert exc_info.value.status_code == 400
    assert "Price cannot be negative" in exc_info.value.detail

def test_create_product_negative_stock(db_session):
    """
    Test that creating a product with a negative stock raises an exception.
    """
    product_data = ProductCreate(
        name="Test Negative Stock",
        description="Testing negative stock",
        price=10.00,
        stock=-2
    )
    with pytest.raises(HTTPException) as exc_info:
        create_product(db_session, product_data)
    assert exc_info.value.status_code == 400
    assert "Stock quantity cannot be negative" in exc_info.value.detail
