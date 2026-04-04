import mysql.connector
from pymongo import MongoClient
import pandas as pd


# ---------------------------
# MySQL Connection
# ---------------------------
mysql_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ecommerce_db",
    port=3306
)

# ---------------------------
# Fetch MySQL Data
# ---------------------------
users_df = pd.read_sql("SELECT * FROM users", mysql_conn)
orders_df = pd.read_sql("SELECT * FROM orders", mysql_conn)
products_df = pd.read_sql("SELECT * FROM products", mysql_conn)

print("Users Data:")
print(users_df.head())

print("\nOrders Data:")
print(orders_df.head())


# ---------------------------
# MongoDB Connection
# ---------------------------
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["ecommerce_db"]
interactions = list(mongo_db["interactions"].find())

interactions_df = pd.DataFrame(interactions)

print("\nInteractions Data:")
print(interactions_df.head())