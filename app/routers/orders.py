from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.database import get_session
from app.schemas import OrderCreate, OrderRead
from app.services.order_service import create_order as create_order_service

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_new_order(
    order_data: OrderCreate, 
    session: Session = Depends(get_session)
):
    """
    Place an order for a list of selected products. 
    Validation, stock checks, and creation happen in the service layer.
    """
    return create_order_service(session, order_data)
