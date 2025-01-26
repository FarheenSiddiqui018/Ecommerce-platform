from typing import List
from pydantic import BaseModel, ConfigDict
from app.enums import StatusEnum


class ProductCreate(BaseModel):
    """
    Schema for creating a new product.
    """

    name: str
    description: str
    price: float
    stock: int


class ProductRead(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock: int

    model_config = ConfigDict(from_attributes=True)


class OrderItem(BaseModel):
    """
    Schema representing an item in an order.
    """

    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    """
    Schema for creating a new order with a list of items.
    """

    products: List[OrderItem]


class OrderRead(BaseModel):
    """
    Schema for reading order information.
    """

    id: int
    total_price: float
    status: StatusEnum
    products: List[ProductRead]

    model_config = ConfigDict(from_attributes=True)
