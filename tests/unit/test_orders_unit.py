# tests/test_orders.py

import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from app.services.order_service import create_order
from app.models import Order
from tests.unit.test_utils import create_order_data


def test_create_order_success(prepopulated_db_session):
    """
    Test successfully creating an order with valid stock.
    """
    order_data = create_order_data(prepopulated_db_session, quantity=3)
    order = create_order(prepopulated_db_session, order_data)

    assert order.id is not None
    assert order.total_price == 10.0 * 3
    assert order.status == "completed"


def test_create_order_insufficient_stock(prepopulated_db_session):
    """
    Test that an HTTP 400 exception is raised if stock is insufficient.
    """
    order_data = create_order_data(prepopulated_db_session, quantity=10)
    with pytest.raises(HTTPException) as exc_info:
        create_order(prepopulated_db_session, order_data)

    assert exc_info.value.status_code == 400
    assert "Insufficient stock" in exc_info.value.detail


def test_create_order_zero_quantity(prepopulated_db_session):
    """
    Test that an HTTP 400 exception is raised if quantity <= 0.
    """
    order_data = create_order_data(prepopulated_db_session, quantity=0)
    with pytest.raises(HTTPException) as exc_info:
        create_order(prepopulated_db_session, order_data)

    assert exc_info.value.status_code == 400
    assert "Quantity must be greater than zero." in exc_info.value.detail


def test_order_invalid_status():
    """
    Ensures the Pydantic field validator for status is triggered (invalid).
    """
    with pytest.raises(ValidationError) as exc_info:
        # Forcibly run Pydantic's validation on the Order model
        Order.model_validate({"status": "wrong"})

    assert "1 validation error for Order" in str(exc_info.value)


def test_order_valid_status():
    """
    Ensures the Pydantic field validator for status accepts a valid status.
    """
    order = Order.model_validate({"status": "completed"})
    assert order.status == "completed"


def test_create_order_invalid_product(db_session):
    """
    Test that an HTTP 404 exception is raised if product is not found.
    """
    from app.schemas import OrderCreate, OrderItem

    order_data = OrderCreate(
        products=[OrderItem(product_id=999, quantity=5)]  # Assuming 999 doesn't exist
    )
    with pytest.raises(HTTPException) as exc_info:
        create_order(db_session, order_data)

    assert exc_info.value.status_code == 404
    assert "Product with ID 999 not found." in exc_info.value.detail
