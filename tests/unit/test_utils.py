# tests/test_utils.py

from typing import Optional
from sqlmodel import Session, select
from app.schemas import OrderCreate, OrderItem, ProductCreate
from app.models import Product


def get_first_product_id(session: Session) -> Optional[int]:
    """
    Retrieves the ID of the first product in the database.
    """
    product_id = session.exec(select(Product.id)).first()
    if product_id is None:
        raise ValueError("No products available in the database.")
    return product_id


def create_order_data(session: Session, quantity: int) -> OrderCreate:
    """
    Creates an OrderCreate instance with a specified quantity.
    """
    product_id = get_first_product_id(session)
    return OrderCreate(products=[OrderItem(product_id=product_id, quantity=quantity)])


def create_product_data(
    name: str, description: str, price: float, stock: int
) -> ProductCreate:
    """
    Creates a ProductCreate instance with the specified parameters.
    """
    return ProductCreate(name=name, description=description, price=price, stock=stock)
