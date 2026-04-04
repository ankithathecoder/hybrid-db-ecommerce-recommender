import random
from datetime import datetime, timedelta

import mysql.connector
from pymongo import MongoClient


# ---------------------------
# 🔗 MySQL Connection
# ---------------------------
mysql_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",   
    database="ecommerce_db",
    port=3306  
)

mysql_cursor = mysql_conn.cursor()


# ---------------------------
# 🍃 MongoDB Connection
# ---------------------------
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["ecommerce_db"]
interaction_collection = mongo_db["interactions"]


# ---------------------------
# 📦 Data Setup
# ---------------------------
NUM_USERS = 50
NUM_PRODUCTS = 100
NUM_ORDERS = 200
NUM_INTERACTIONS = 1000

categories = ["electronics", "fashion", "books", "home", "sports"]
events = ["view", "search", "add_to_cart"]


# ---------------------------
# 👤 Generate Users
# ---------------------------
users = []
for i in range(1, NUM_USERS + 1):
    name = f"User{i}"
    email = f"user{i}@gmail.com"
    users.append((i, name, email))

mysql_cursor.executemany(
    "INSERT INTO users (user_id, name, email) VALUES (%s, %s, %s)",
    users
)


# ---------------------------
# 🛍️ Generate Products
# ---------------------------
products = []
for i in range(1, NUM_PRODUCTS + 1):
    category = random.choice(categories)
    name = f"{category}_product_{i}"
    products.append((i, name, category))

mysql_cursor.executemany(
    "INSERT INTO products (product_id, name, category) VALUES (%s, %s, %s)",
    products
)


# ---------------------------
# 💰 Generate Orders
# ---------------------------
orders = []
for i in range(1, NUM_ORDERS + 1):
    user_id = random.randint(1, NUM_USERS)
    product_id = random.randint(1, NUM_PRODUCTS)
    amount = round(random.uniform(100, 5000), 2)

    order_date = datetime.now() - timedelta(days=random.randint(1, 30))

    orders.append((i, user_id, product_id, amount, order_date))

mysql_cursor.executemany(
    """
    INSERT INTO orders (order_id, user_id, product_id, amount, order_date)
    VALUES (%s, %s, %s, %s, %s)
    """,
    orders
)


# ---------------------------
# 🍃 Generate MongoDB Interactions
# ---------------------------
interactions = []

for _ in range(NUM_INTERACTIONS):
    user_id = random.randint(1, NUM_USERS)
    product_id = random.randint(1, NUM_PRODUCTS)
    event = random.choice(events)
    category = random.choice(categories)

    interaction = {
        "user_id": user_id,
        "product_id": product_id,
        "event": event,
        "category": category,
        "timestamp": datetime.now() - timedelta(days=random.randint(1, 30))
    }

    interactions.append(interaction)

interaction_collection.insert_many(interactions)


# ---------------------------
# ✅ Commit & Close
# ---------------------------
mysql_conn.commit()
mysql_cursor.close()
mysql_conn.close()

print("✅ Data generation complete!")