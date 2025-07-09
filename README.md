# bmtc-route-recommender
# 🚍 BMTC Route Recommender

A **Streamlit web app** to recommend BMTC (Bangalore Metropolitan Transport Corporation) bus routes based on an Excel file containing bus route data in JSON format.

---

## 📌 Features

- Upload `.xlsx` file with BMTC route data
- Extracts bus stops from JSON column
- Select origin and destination stops
- Recommends routes with up to **3 hops**
- Simple and clean UI built with Streamlit

---

## 📂 Input Format

Your Excel file **must contain** a column named `map_json_content`.  
Each row in that column should be a **JSON array** of stops like:

```json
[
  {"busstop": "Majestic, Bangalore"},
  {"busstop": "Vijayanagar, Bangalore"},
  {"busstop": "Rajajinagar, Bangalore"}
]
