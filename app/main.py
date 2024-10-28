# app/main.py

from fastapi import FastAPI
from app.routers import service_order, tool_usage, manual, user_orders
from app.auth import auth

app = FastAPI()

# Incluir os roteadores
app.include_router(auth.router)
app.include_router(service_order.router)
app.include_router(tool_usage.router)
app.include_router(manual.router)
app.include_router(user_orders.router)
