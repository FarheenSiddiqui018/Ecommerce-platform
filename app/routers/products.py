from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
from app.schemas import ProductCreate, ProductRead
from app.services.product_service import list_products, create_product

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductRead])
def read_products(session: Session = Depends(get_session)):
    """
    Retrieve a list of all available products.
    """
    print("DEBUG: Using DB:", session.bind.url)
    return list_products(session)


@router.post("", response_model=ProductRead, status_code=201)
def add_product(product_data: ProductCreate, session: Session = Depends(get_session)):
    """
    Add a new product to the platform.
    """
    return create_product(session, product_data)
