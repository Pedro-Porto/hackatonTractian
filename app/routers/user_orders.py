# app/routers/user_orders.py

from fastapi import APIRouter, Depends, Query
from app.models import User
from app.auth.auth import get_current_user
from app.database import orders_collection

router = APIRouter()

@router.get("/userOrders")
async def user_orders(
    username: str = Query(...)
    # current_user: User = Depends(get_current_user)
):
    user_orders = orders_collection.find_one({"username": username})
    from app.database import tools_collection
    
    if user_orders:
        tools_list = list(tools_collection.find({}))

        tools = [
            {
                "toolName": tool.get("toolName"),
                "sapCode": tool.get("sapCode"),
                "schedule": tool.get("schedule", [])
            }
            for tool in tools_list
        ]

        uOrders = user_orders.get("orders", [])

        for order in uOrders:
            order['order']["tools"] = tools

        return uOrders
    else:
        return []

