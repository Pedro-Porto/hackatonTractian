# app/routers/tool_usage.py

from fastapi import APIRouter, Depends, Body
from typing import List
from app.models import ToolUsage, User
from app.auth.auth import get_current_user
from app.database import tools_collection

router = APIRouter()

@router.post("/toolUsage")
async def tool_usage(
    data: List[ToolUsage] = Body(...), current_user: User = Depends(get_current_user)
):
    for usage in data:
        tools_collection.update_one(
            {"sapCode": usage.toolCode},
            {"$push": {"schedule": {
                "startTime": usage.startTime,
                "endTime": usage.endTime,
                "user": usage.username
            }}}
        )
    return {"message": "Tool usage updated"}
