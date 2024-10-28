# app/routers/manual.py

from fastapi import APIRouter, Depends, Query
from app.models import User
from app.auth.auth import get_current_user
from app.database import manuals_collection

router = APIRouter()

@router.get("/manual")
async def get_manual(
    machineId: int = Query(...), current_user: User = Depends(get_current_user)
):
    # Buscar a ordem atual no banco de dados
    # Enviar para a LLM com o ID da máquina para sumarizar os manuais dessa máquina
    # Implementação de exemplo
    manuals = list(manuals_collection.find({"machineId": machineId}))
    # Chamar a LLM para sumarizar os manuais
    summaries = "Summarized manuals content"
    return {
        "manuals": manuals,
        "videos": [],
        "summaries": summaries,
        "suggestions": []
    }
