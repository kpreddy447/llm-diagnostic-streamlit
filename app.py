import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image
import os
from analysis import analyze_graphs
from importdata import load_data_from_csv
# Config

st.set_page_config(layout="wide")
st.title("Latency Analysis — Success vs Failure")

st.sidebar.header("Input Parameters")
df = load_data_from_csv("bing_maps_telemetry_50000.csv")
# Get filter options from the dataframe (assuming df is your filtered dataset)
operation_options = df['operation'].dropna().unique().tolist()
browser_options = df['browser'].dropna().unique().tolist()
os_options = df['os'].dropna().unique().tolist()

# Sidebar filters
selected_operations = st.sidebar.multiselect(
    "Filter by Operation",
    options=sorted(operation_options),
    help="Select one or more API operations (e.g. Geocode, GetElevation)"
)

selected_browsers = st.sidebar.multiselect(
    "Filter by Browser",
    options=sorted(browser_options),
    help="Select one or more browsers (e.g. Chrome, Edge)"
)

selected_oses = st.sidebar.multiselect(
    "Filter by Operating System",
    options=sorted(os_options),
    help="Select one or more OS types (e.g. Windows 11, macOS)"
)



# Session state
if "chart_paths" not in st.session_state:
    st.session_state.chart_paths = {"path1": None, "path2": None}

# Load data
@st.cache_data
def load_data(csv_file):
    df = pd.read_csv(csv_file, parse_dates=["timestamp"])
    if df["timestamp"].dt.tz is None:
        df["timestamp"] = df["timestamp"].dt.tz_localize("UTC")
    return df

csv_file = "bing_maps_telemetry_50000.csv"
df = load_data(csv_file)

# Date inputs
col1, col2 = st.columns(2)
with col1:
    start_date_1 = st.sidebar.date_input("Start Date (Period 1)")
    end_date_1 = st.sidebar.date_input("End Date (Period 1)")
with col2:
    start_date_2 = st.sidebar.date_input("Start Date (Period 2)")
    end_date_2 = st.sidebar.date_input("End Date (Period 2)")

# Make timezone-aware
start_date_1 = pd.to_datetime(start_date_1).tz_localize("UTC")
end_date_1 = pd.to_datetime(end_date_1).tz_localize("UTC")
start_date_2 = pd.to_datetime(start_date_2).tz_localize("UTC")
end_date_2 = pd.to_datetime(end_date_2).tz_localize("UTC")
if start_date_1 > end_date_1 or start_date_2 > end_date_2:
    st.error("Start date must be before end date for both periods.")
    st.stop()

# Filter the dataframe based on selected values
if selected_operations:
    df = df[df['operation'].isin(selected_operations)]

if selected_browsers:
    df = df[df['browser'].isin(selected_browsers)]

if selected_oses:
    df = df[df['os'].isin(selected_oses)]


# Generate graphs
def generate_latency_by_hour_plot(data, title, filename):
    data['hour'] = data['timestamp'].dt.hour
    data['day_of_week'] = data['timestamp'].dt.day_name()

    sns.set(style='whitegrid', palette='muted')
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=data, x='hour', y='latencyMs', hue='status', errorbar=None)

    plt.title(title)
    plt.xlabel("Hour of Day (0–23)")
    plt.ylabel("Latency (ms)")
    plt.legend(title="Status")
    plt.xticks(range(0, 24))
    plt.tight_layout()

    os.makedirs("charts", exist_ok=True)
    filepath = os.path.join("charts", filename)
    plt.savefig(filepath)
    plt.close()
    return filepath

if st.button("Generate Comparison Chart"):
    df1 = df[(df["timestamp"] >= start_date_1) & (df["timestamp"] <= end_date_1)].copy()
    df2 = df[(df["timestamp"] >= start_date_2) & (df["timestamp"] <= end_date_2)].copy()
    if df1.empty or df2.empty:
        st.error("No data found for one or both selected periods. Adjust your filters or date ranges.")
        st.stop()
    path1 = generate_latency_by_hour_plot(df1, "Latency by Hour — Period 1", "latency_period1.png")
    path2 = generate_latency_by_hour_plot(df2, "Latency by Hour — Period 2", "latency_period2.png")

    st.session_state.chart_paths["path1"] = path1
    st.session_state.chart_paths["path2"] = path2

# Load chart paths
path1 = st.session_state.chart_paths.get("path1")
path2 = st.session_state.chart_paths.get("path2")

# Show in sidebar
col1, col2 = st.columns(2)
with col1:
    if path1 and os.path.exists(path1):
        st.image(Image.open(path1), caption="Graph 1", use_container_width=True)
with col2:    
    if path2 and os.path.exists(path2):
        st.image(Image.open(path2), caption="Graph 2", use_container_width=True)

# Compare with LLM
if path1 and path2:
    if st.button("Compare Graphs"):
        with st.spinner("Analyzing..."):
            result = analyze_graphs(
                path1, path2,
                start_date_1=start_date_1,
                end_date_1=end_date_1,
                start_date_2=start_date_2,
                end_date_2=end_date_2
            )
        st.markdown("### Comparison Summary")
        st.write(result)
