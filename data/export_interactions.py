import pandas as pd
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["ecommerce_db"]

# Read interactions collection
interactions = list(db["interactions"].find())
df = pd.DataFrame(interactions)

# Optional: drop MongoDB _id column
df = df.drop(columns=["_id"], errors="ignore")

# Save to CSV
df.to_csv("data/interactions.csv", index=False)

print("✅ interactions.csv saved!")