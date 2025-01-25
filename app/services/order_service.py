from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models import Order, Product, ProductOrderLink
from app.schemas import OrderCreate

def create_order(session: Session, order_data: OrderCreate):
    """
    Place an order for a list of selected products. 
    Validate sufficient stock for each item and create the order.
    """
    # Initialize the order
    order = Order(status="pending", total_price=0.0)
    session.add(order)
    session.commit()
    session.refresh(order)

    total_price = 0.0

    # Process each product item in the order
    for item in order_data.products:
        # Fetch the product from the database
        product = session.exec(select(Product).where(Product.id == item.product_id)).one_or_none()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {item.product_id} not found."
            )
        if item.quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantity must be greater than zero."
            )
        # Check stock availability
        if product.stock < item.quantity:
            session.rollback()  # Rollback if any product fails
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for product {product.name}."
            )

        # Deduct stock
        product.stock -= item.quantity

        # Calculate cost
        cost = product.price * item.quantity
        total_price += cost

        # Create the association in the link table
        link = ProductOrderLink(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity
        )
        session.add(link)

    order.total_price = total_price

    # For simplicity, assume we complete the order immediately
    order.status = "completed"

    session.add(order)
    session.commit()
    session.refresh(order)

    return order
