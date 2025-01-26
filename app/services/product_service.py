from sqlmodel import select, Session
from fastapi import HTTPException, status

from app.models import Product
from app.schemas import ProductCreate


def list_products(session: Session):
    """
    Fetch all products from the database.
    """
    return session.exec(select(Product)).all()


def create_product(session: Session, product_data: ProductCreate):
    """
    Validate and create a new product in the database.
    """
    # Validate basic constraints
    if product_data.price <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Price cannot be negative or zero.",
        )
    if product_data.stock < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Stock quantity cannot be negative.",
        )

    # Create the product
    new_product = Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        stock=product_data.stock,
    )
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product
