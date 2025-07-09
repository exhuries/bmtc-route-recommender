import streamlit as st
import pandas as pd
import json
from collections import defaultdict, deque

@st.cache_data
def load_data(file):
    df = pd.read_excel(file)
    df.columns = df.columns.str.strip().str.lower()
    if "map_json_content" not in df.columns:
        st.error("Missing 'map_json_content' column in uploaded file.")
        return pd.DataFrame()
    df = df[df["map_json_content"].notna()]

    # Extract clean stop names
    def extract_stops(json_str):
        try:
            stops = json.loads(json_str)
            return [stop['busstop'].split(",")[0].strip() for stop in stops]
        except:
            return []

    df["stop_names"] = df["map_json_content"].apply(extract_stops)
    return df

def build_stop_map(df):
    stop_to_routes = defaultdict(list)
    for idx, row in df.iterrows():
        for stop in row["stop_names"]:
            stop_to_routes[stop].append(idx)
    return stop_to_routes

def find_routes(df, stop_to_routes, source, destination, max_hops=3):
    visited = set()
    queue = deque([(source, [])])  # (current_stop, path_so_far)

    while queue:
        current_stop, path = queue.popleft()
        if len(path) > max_hops:
            continue

        for route_idx in stop_to_routes.get(current_stop, []):
            route = df.iloc[route_idx]
            stops = route["stop_names"]
            if destination in stops:
                return path + [(route["route_no"], current_stop, destination)]
            for next_stop in stops:
                if next_stop not in visited:
                    visited.add(next_stop)
                    queue.append((next_stop, path + [(route["route_no"], current_stop, next_stop)]))
    return None

# Streamlit App
st.set_page_config(page_title="BMTC Route Recommender")
st.title("🚍 BMTC Bus Route Recommender")

uploaded_file = st.file_uploader("📂 Upload your BMTC Excel file", type=["xlsx"])

if uploaded_file:
    df = load_data(uploaded_file)
    if not df.empty:
        stop_to_routes = build_stop_map(df)
        unique_stops = sorted(stop_to_routes.keys())

        origin = st.selectbox("🛫 Choose Origin Stop", unique_stops)
        destination = st.selectbox("🏁 Choose Destination Stop", unique_stops)

        if st.button("🔍 Find Routes"):
            with st.spinner("Searching routes..."):
                result = find_routes(df, stop_to_routes, origin, destination)
            if result:
                st.success("✅ Route(s) found:")
                for route in result:
                    st.markdown(f"- 🚌 Route **{route[0]}**: {route[1]} ➡️ {route[2]}")
            else:
                st.error("❌ No routes found between selected stops.")
    else:
        st.warning("Please upload a valid Excel file with `map_json_content` column.")
else:
    st.info("Upload your `.xlsx` file to begin.")
