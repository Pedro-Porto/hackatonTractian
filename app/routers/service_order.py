# app/routers/service_order.py

from fastapi import APIRouter, Depends, UploadFile, File, Body
from app.models import ServiceOrderData, EquipmentData, User
from app.auth.auth import get_current_user
from app.utils.helpers import fillServiceOrder

router = APIRouter()

@router.post("/serviceOrder/audio")
async def service_order_audio(
    file: UploadFile = File(...)#, current_user: User = Depends(get_current_user)
):
    order_text = "" 
    equipment_data = fillServiceOrder(order_text)
    return equipment_data

@router.post("/serviceOrder/text")
async def service_order_text(
    data: ServiceOrderData = Body(...)#, current_user: User = Depends(get_current_user)
):
    equipment_data = fillServiceOrder(data.orderText)

    return equipment_data
