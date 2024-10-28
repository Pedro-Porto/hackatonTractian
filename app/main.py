from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import service_order, tool_usage, manual, user_orders
from app.auth import auth

app = FastAPI()

# Configurar as origens permitidas
origins = [
    "http://localhost:5173",  
]

# Adicionar o middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            
    allow_credentials=True,           
    allow_methods=["*"],              
    allow_headers=["*"],              
)

# Incluir os roteadores
app.include_router(auth.router)
app.include_router(service_order.router)
app.include_router(tool_usage.router)
app.include_router(manual.router)
app.include_router(user_orders.router)
