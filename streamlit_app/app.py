import os
import streamlit as st
import pandas as pd

#  CSS
st.markdown("""
<style>

/* ================================
   SIDEBAR (FILTER PANEL)
================================ */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0E1117 0%, #0B0F14 100%);
    border-right: 1px solid #1f2937;
}

/* FILTER CONTAINERS */
section[data-testid="stSidebar"] .stMultiSelect,
section[data-testid="stSidebar"] .stTextInput {
    background-color: #111827;
    border-radius: 12px;
    padding: 6px;
    transition: all 0.25s ease;
}

/* HOVER GLOW */
section[data-testid="stSidebar"] .stMultiSelect:hover,
section[data-testid="stSidebar"] .stTextInput:hover {
    box-shadow: 0 0 14px rgba(0, 230, 118, 0.45);
    transform: translateY(-1px);
}

/* SELECTED TAGS (CHIPS) */
span[data-baseweb="tag"] {
    background-color: #00E676 !important;
    color: #0E1117 !important;
    font-weight: 600;
    border-radius: 6px;
}

/* ================================
   KPI CARDS
================================ */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #111827, #0B0F14);
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #1f2937;
    box-shadow: 0 4px 18px rgba(0,0,0,0.35);
}

/* ================================
   TABLE STYLING
================================ */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    border: 1px solid #1f2937;
}

</style>
""", unsafe_allow_html=True)
 
# =====================================
# Import Dashboard Sections
# =====================================
from ui.overall import overall_dashboard
from ui.vehicle_type import vehicle_type_dashboard
from ui.revenue import revenue_dashboard
from ui.cancellation import cancellation_dashboard
from ui.ratings import ratings_dashboard

# =====================================
# Page Configuration
# =====================================
st.set_page_config(
    page_title="OLA Ride Analytics",
    layout="wide"
)

st.title("🚖 OLA Ride Analytics Dashboard")


# =====================================
# Dashboard Tabs (PPT → Streamlit)
# =====================================
tabs = st.tabs([
    "Overall",
    "Vehicle Type",
    "Revenue",
    "Cancellation",
    "Ratings"
])

# =====================================
# Load Data (CSV – Deployment Ready)
# =====================================
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir,"OLA_Rides_Riview.csv")
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
# Apply Filters (DEFINE filtered_df ONCE)
# =====================================
filtered_df = df.copy()

if status_filter:
    filtered_df = filtered_df[
        filtered_df["booking_status"].isin(status_filter)
    ]

if vehicle_filter:
    filtered_df = filtered_df[
        filtered_df["vehicle_type"].isin(vehicle_filter)
    ]

if payment_filter:
    filtered_df = filtered_df[
        filtered_df["payment_method"].isin(payment_filter)
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
# KPI CALCULATIONS (KEEPED GLOBAL – CORRECT)
# =====================================
total_rides = filtered_df.shape[0]

completed_rides = filtered_df[
    (filtered_df["booking_status"] == "Success") &
    (filtered_df["incomplete_rides"] == "No")
].shape[0]

incomplete_rides = filtered_df[
    filtered_df["incomplete_rides"] == "Yes"
].shape[0]

cancelled_rides = filtered_df[
    filtered_df["booking_status"].str.contains("Cancelled", case=False, na=False)
].shape[0]

cancellation_rate = (
    round((cancelled_rides / total_rides) * 100, 2)
    if total_rides > 0 else 0.0
)

avg_customer_rating = round(
    filtered_df[
        (filtered_df["booking_status"] == "Success") &
        (filtered_df["incomplete_rides"] == "No")
    ]["customer_rating"].mean(),
    2
)

# =====================================
# TAB 1: OVERALL DASHBOARD
# =====================================
with tabs[0]:
    st.subheader("📈 Key Metrics")


    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Total Rides", total_rides)
    col2.metric("Completed Rides", completed_rides)
    col3.metric("Incomplete Rides", incomplete_rides)
    col4.metric("Cancelled Rides", cancelled_rides)
    col5.metric("Cancellation Rate (%)", cancellation_rate)

    st.caption(
        "Note: Successful bookings with incomplete rides (e.g., Customer Demand) "
        "are excluded from Completed Rides and tracked separately."
    )

    st.divider()
    st.subheader("📄 Ride Data Preview")
    st.dataframe(filtered_df, use_container_width=True)

    st.divider()
    overall_dashboard(filtered_df)

# =====================================
# TAB 2: VEHICLE TYPE
# =====================================
with tabs[1]:
    vehicle_type_dashboard(filtered_df)


# =====================================
# TAB 3: REVENUE
# =====================================
with tabs[2]:
    revenue_dashboard(filtered_df)

# =====================================
# TAB 4: CANCELLATION
# =====================================
with tabs[3]:
    cancellation_dashboard(filtered_df)

# =====================================
# TAB 5: RATINGS
# =====================================
with tabs[4]:
    ratings_dashboard(filtered_df)

# =====================================
# Footer
# =====================================
st.divider()
st.caption("Built with Streamlit • Python • Data sourced from cleaned CSV")
