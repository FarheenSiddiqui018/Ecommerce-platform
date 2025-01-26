from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from .enums import StatusEnum


class ProductOrderLink(SQLModel, table=True):
    """
    Association table for many-to-many relationship between Order and Product.
    Includes quantity field to store how many of each product are in an order.
    """

    order_id: Optional[int] = Field(
        default=None, foreign_key="order.id", primary_key=True
    )
    product_id: Optional[int] = Field(
        default=None, foreign_key="product.id", primary_key=True
    )
    quantity: int = Field(default=1)


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str
    description: str
    price: float
    stock: int

    # Relationship back to Order via the link table
    orders: List["Order"] = Relationship(
        back_populates="products", link_model=ProductOrderLink
    )


class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    total_price: float = Field(default=0.0)
    status: StatusEnum = Field(default=StatusEnum.pending)

    # Relationship to Product via the link table
    products: List[Product] = Relationship(
        back_populates="orders", link_model=ProductOrderLink
    )
