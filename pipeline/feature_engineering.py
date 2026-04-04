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

# Fetch data
orders_df = pd.read_sql("SELECT * FROM orders", mysql_conn)

products_df = pd.read_sql("SELECT * FROM products", mysql_conn)
# ---------------------------
# MongoDB Connection
# ---------------------------
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["ecommerce_db"]

interactions = list(mongo_db["interactions"].find())
interactions_df = pd.DataFrame(interactions)

# ---------------------------
# Category-wise Views
# ---------------------------
view_counts = (
    interactions_df[interactions_df["event"] == "view"]
    .groupby(["user_id", "category"])
    .size()
    .unstack(fill_value=0)
)

view_counts.columns = [f"views_{col}" for col in view_counts.columns]


# ---------------------------
# Category-wise Purchases
# ---------------------------
orders_with_category = orders_df.merge(products_df, on="product_id")

purchase_counts = (
    orders_with_category.groupby(["user_id", "category"])
    .size()
    .unstack(fill_value=0)
)

purchase_counts.columns = [f"purchases_{col}" for col in purchase_counts.columns]


# ---------------------------
# Merge features
# ---------------------------
features_df = view_counts.merge(purchase_counts, on="user_id", how="outer").fillna(0)


# ---------------------------
# Target (y)
# ---------------------------
# Most purchased category (better than viewed)
target = (
    orders_with_category.groupby(["user_id", "category"])
    .size()
    .reset_index(name="count")
)

target = target.sort_values(["user_id", "count"], ascending=[True, False])
target = target.drop_duplicates("user_id")[["user_id", "category"]]

features_df = features_df.merge(target, on="user_id", how="left")
features_df.rename(columns={"category": "target_category"}, inplace=True)

print(features_df.head())