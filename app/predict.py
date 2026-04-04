import pickle
import pandas as pd
import mysql.connector
from pymongo import MongoClient


# ---------------------------
# 🔗 Load Model
# ---------------------------
with open("model/model.pkl", "rb") as f:
    model, label_encoder, feature_columns = pickle.load(f)


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

orders_df = pd.read_sql("SELECT * FROM orders", mysql_conn)
products_df = pd.read_sql("SELECT * FROM products", mysql_conn)


# ---------------------------
# 🔗 MongoDB Connection
# ---------------------------
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["ecommerce_db"]

interactions = list(mongo_db["interactions"].find())
interactions_df = pd.DataFrame(interactions)


# ---------------------------
# 🎯 Get ALL possible categories
# ---------------------------
all_categories = products_df["category"].unique()


# ---------------------------
# 🎯 Feature builder for ONE user
# ---------------------------
def get_user_features(user_id):
    # Initialize feature dict
    features = {}

    # ---- Views ----
    user_views = interactions_df[
        (interactions_df["user_id"] == user_id) &
        (interactions_df["event"] == "view")
    ]

    view_counts = user_views["category"].value_counts()

    for cat in all_categories:
        features[f"views_{cat}"] = view_counts.get(cat, 0)


    # ---- Purchases ----
    user_orders = orders_df[orders_df["user_id"] == user_id]
    user_orders = user_orders.merge(products_df, on="product_id")

    purchase_counts = user_orders["category"].value_counts()

    for cat in all_categories:
        features[f"purchases_{cat}"] = purchase_counts.get(cat, 0)


    return pd.DataFrame([features])


# ---------------------------
# 🔮 Prediction Function
# ---------------------------
def predict_category(user_id):
    features = get_user_features(user_id)

    for col in feature_columns:
        if col not in features:
            features[col] = 0

    features = features[feature_columns]

    prediction = model.predict(features)
    category = label_encoder.inverse_transform(prediction)

    return category[0]


# ---------------------------
# ▶️ Run
# ---------------------------
if __name__ == "__main__":
    user_id = int(input("Enter User ID: "))

    result = predict_category(user_id)

    print(f"\n🎯 Recommended Category: {result}")