# Ecommerce Recommendation System Using Hybrid Databases

## Overview
This project is a **hybrid database-powered e-commerce recommendation system**. It combines **MySQL** (for structured user, product, and order data) and **MongoDB** (for user interactions like views, searches, and cart events) to generate personalized product category recommendations using **Machine Learning (Logistic Regression)**.  

The system also features a **Streamlit interface** for interactive predictions and can be visualized using **Power BI** for deeper insights.

---

## Features
- Stores e-commerce data in **MySQL** and **MongoDB**.  
- **Data extraction** and **feature engineering** pipelines prepare the dataset for ML.  
- Machine Learning model predicts the most likely **product category** a user will interact with.  
- Streamlit interface for easy **user interaction and category prediction**.  
- Supports **offline analysis** using CSV exports from both databases.  
- Visualizable using **Power BI** for dashboards of users, orders, products, and interactions.

---

## Tech Stack
- **Python** – Main programming language  
- **MySQL** – Structured database for users, products, and orders  
- **MongoDB** – NoSQL database for interactions  
- **Pandas / Scikit-learn** – Data processing and ML  
- **Streamlit** – Frontend UI for predictions  
- **Power BI** – Dashboard visualizations (optional)  

---

## Screenshots
**Invalid User ID**: app/output/invalid_UserID.png
**Valid User ID**: app/output/valid_UserID.png

---

## Future Improvements
Upgrade Streamlit frontend with multi-page UI and visualizations.
Real-time recommendation updates when database changes.
Deploy to Heroku / Streamlit Cloud for online access.
