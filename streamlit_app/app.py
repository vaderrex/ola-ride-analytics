import os
import streamlit as st
import pandas as pd

# =====================================
# Page Configuration
# =====================================
st.set_page_config(
    page_title="OLA Ride Analytics",
    layout="wide"
)

st.title("🚖 OLA Ride Analytics Dashboard")

# =====================================
# Load Data (CSV – Deployment Ready)
# =====================================
def load_data():
    base_dir = os.path.dirname(__file__)  # points to streamlit_app/
    file_path = os.path.join(base_dir, "OLA_Rides_Riview.csv")
    return pd.read_csv(file_path)
df = load_data()

# =====================================
# Data Cleanup (Presentation Layer Only)
# =====================================
df = df.drop(columns=["vehicle_images", "unnamed_20"], errors="ignore")

# =====================================
# Sidebar Filters
# =====================================
st.sidebar.header("🔍 Filters")

status_filter = st.sidebar.multiselect(
    "Booking Status",
    options=df["booking_status"].dropna().unique(),
    default=df["booking_status"].dropna().unique()
)

vehicle_filter = st.sidebar.multiselect(
    "Vehicle Type",
    options=df["vehicle_type"].dropna().unique(),
    default=df["vehicle_type"].dropna().unique()
)

payment_filter = st.sidebar.multiselect(
    "Payment Method",
    options=df["payment_method"].dropna().unique(),
    default=df["payment_method"].dropna().unique()
)

# =====================================
# Apply Filters
# =====================================
filtered_df = df[
    (df["booking_status"].isin(status_filter)) &
    (df["vehicle_type"].isin(vehicle_filter)) &
    (df["payment_method"].isin(payment_filter))
]

# =====================================
# Search Booking ID
# =====================================
search_id = st.text_input("🔎 Search Booking ID")

if search_id:
    filtered_df = filtered_df[
        filtered_df["booking_id"].astype(str).str.contains(search_id)
    ]

# =====================================
# Key Metrics
# =====================================
st.divider()
st.subheader("📊 Key Metrics")

total_rides = filtered_df.shape[0]

completed_rides = df_filtered[
    (df_filtered["booking_status"] == "Success") &
    (df_filtered["incomplete_rides"] == "No")
].shape[0]

cancelled_rides = filtered_df[
    filtered_df["booking_status"] != "Success"
].shape[0]

cancellation_rate = (
    round((cancelled_rides / total_rides) * 100, 2)
    if total_rides > 0 else 0
)

avg_customer_rating = round(
    filtered_df[
        filtered_df["booking_status"] == "Success"
    ]["customer_rating"].mean(),
    2
)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Rides", total_rides)
col2.metric("Completed Rides", completed_rides)
col3.metric("Cancelled Rides", cancelled_rides)
col4.metric("Cancellation Rate (%)", cancellation_rate)
col5.metric("Avg Customer Rating", avg_customer_rating)

# =====================================
# Data Preview
# =====================================
st.divider()
st.subheader("📄 Ride Data Preview")
st.dataframe(filtered_df, width="stretch")

# =====================================
# Footer
# =====================================
st.divider()
st.caption("Built with Streamlit • Python (Data sourced from cleaned CSV)")
