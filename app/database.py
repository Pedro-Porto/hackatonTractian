# app/database.py

from pymongo import MongoClient
from app.config import DATABASE_URL

client = MongoClient(DATABASE_URL)
db = client.main

print(client.list_database_names())

# Definir as coleções
users_collection = db.users
orders_collection = db.orders
tools_collection = db.tools
manuals_collection = db.manuals
