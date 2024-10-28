# app/routers/user_orders.py

from fastapi import APIRouter, Depends
from app.models import User
from app.auth.auth import get_current_user
from app.database import orders_collection

router = APIRouter()

@router.get("/userOrders")
async def user_orders(
    current_user: User = Depends(get_current_user)
):
    # Pegar no banco de dados todas as ordens antigas
    user_orders = orders_collection.find_one({"username": current_user.username})
    if user_orders:
        return user_orders.get("orders", [])
    else:
        return []
