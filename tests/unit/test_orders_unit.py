import pytest
from fastapi import HTTPException
from pydantic import ValidationError
from sqlmodel import Session, select

from app.schemas import OrderCreate, OrderItem
from app.services.order_service import create_order
from app.models import Product, Order

@pytest.fixture
def db_session():
    """
    This fixture creates a session on the shared in-memory test DB, 
    inserts a Product, and yields the session for the test.
    """
    from tests.conftest import test_engine
    with Session(test_engine) as session:
        # Insert a product so we can test orders
        product = Product(name="Widget", description="A widget", price=10.0, stock=5)
        session.add(product)
        session.commit()
        session.refresh(product)
        yield session

def test_create_order_success(db_session):
    """
    Test successfully creating an order with valid stock.
    """
    product_id = db_session.exec(select(Product.id)).first()
    order_data = OrderCreate(
        products=[OrderItem(product_id=product_id, quantity=3)]
    )
    order = create_order(db_session, order_data)

    assert order.id is not None
    assert order.total_price == 10.0 * 3
    assert order.status == "completed"

def test_create_order_insufficient_stock(db_session):
    """
    Test that an HTTP 400 exception is raised if stock is insufficient.
    """
    product_id = db_session.exec(select(Product.id)).first()
    order_data = OrderCreate(
        products=[OrderItem(product_id=product_id, quantity=10)]
    )
    with pytest.raises(HTTPException) as exc_info:
        create_order(db_session, order_data)

    assert exc_info.value.status_code == 400
    assert "Insufficient stock" in exc_info.value.detail

def test_create_order_zero_quantity(db_session):
    """
    Test that an HTTP 400 exception is raised if quantity <= 0.
    """
    product_id = db_session.exec(select(Product.id)).first()
    order_data = OrderCreate(
        products=[OrderItem(product_id=product_id, quantity=0)]
    )
    with pytest.raises(HTTPException) as exc_info:
        create_order(db_session, order_data)

    assert exc_info.value.status_code == 400
    assert "Quantity must be greater than zero." in exc_info.value.detail

def test_order_invalid_status():
    """
    Ensures the Pydantic field validator for status is triggered (invalid).
    """
    with pytest.raises(ValidationError) as exc_info:
        # forcibly run pydantic's validation on the Order model
        Order.model_validate({"status": "wrong"})

    assert "Status must be one of" in str(exc_info.value)

def test_order_valid_status():
    """
    Ensures the Pydantic field validator for status accepts a valid status.
    """
    order = Order.model_validate({"status": "completed"})
    assert order.status == "completed"

def test_create_order_invalid_product(db_session):
    """
    Test that an HTTP 404 exception is raised if product is not found
    """
    order_data = OrderCreate(
        products=[OrderItem(product_id=4, quantity=5)]
    )
    with pytest.raises(HTTPException) as exc_info:
        create_order(db_session, order_data)

    assert exc_info.value.status_code == 404
    assert "Product with ID 4 not found." in exc_info.value.detail
