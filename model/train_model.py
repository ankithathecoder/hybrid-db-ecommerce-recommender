import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
import pickle

# Import your feature file
from pipeline.feature_engineering import features_df


# ---------------------------
# Prepare Data
# ---------------------------

# Input features
X = features_df.drop(columns=["user_id", "target_category"])

# Target variable
y = features_df["target_category"]

# Convert category to numbers
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)


# ---------------------------
# Train Model
# ---------------------------
model = LogisticRegression(max_iter=200)
model.fit(X, y_encoded)

# ---------------------------
# Save Model
# ---------------------------
feature_columns = X.columns.tolist()

with open("model/model.pkl", "wb") as f:
    pickle.dump((model, label_encoder, feature_columns), f)


print("✅ Model trained and saved!")