# app/database.py

from pymongo import MongoClient
from app.config import DATABASE_URL

client = MongoClient(DATABASE_URL)
db = client.get_default_database()

# Definir as coleções
users_collection = db.users
orders_collection = db.orders
tools_collection = db.tools
manuals_collection = db.manuals
