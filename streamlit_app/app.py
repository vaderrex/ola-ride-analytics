import os
import streamlit as st
import pandas as pd
# =====================================
# LOAD LOGO
# =====================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "assets","ola_logo.png")
st.image(LOGO_PATH, width=300)

# =====================================
# PAGE CONFIG (MUST BE FIRST STREAMLIT CALL)
# =====================================
st.set_page_config(
    page_title="OLA Ride Analytics",
    layout="wide"
)

# =====================================
# ADVANCED UI CSS
# =====================================
st.markdown("""
<style>

/* ================================
   MAIN APP BACKGROUND
================================ */
.stApp {
    background: linear-gradient(135deg, #020617, #020b1c, #020617);
    color: #e5e7eb;
}

/* ================================
   SIDEBAR (LIGHTER FOR LOGO VISIBILITY)
================================ */
section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #7c91c2 0%,
        #0b1220 100%
    );
    border-right: 1px solid #1f2937;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: #e5e7eb;
}

/* ================================
   SIDEBAR FILTER CONTAINERS
================================ */
section[data-testid="stSidebar"] .stMultiSelect,
section[data-testid="stSidebar"] .stTextInput,
section[data-testid="stSidebar"] .stSlider {
    background-color: #020b1c;
    border-radius: 12px;
    padding: 6px;
}

/* Selected chips */
span[data-baseweb="tag"] {
    background-color: #00E676 !important;
    color: #020617 !important;
    font-weight: 600;
    border-radius: 6px;
}

/* ================================
   KPI CARDS
================================ */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #020b1c, #020617);
    padding: 18px;
    border-radius: 16px;
    border: 1px solid #1f2937;
    box-shadow: 0 6px 22px rgba(0,0,0,0.45);
}

/* ================================
   TABLE STYLING
================================ */
[data-testid="stDataFrame"] {
    border-radius: 14px;
    border: 1px solid #1f2937;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <div style="
        background-color:#020617;
        padding:16px;
        border-radius:12px;
        text-align:center;
        margin-top:0px;
        margin-bottom:12px;
    ">
    """,
    unsafe_allow_html=True
)

# =====================================
# IMPORT DASHBOARD SECTIONS
# =====================================
from ui.overall import overall_dashboard
from ui.vehicle_type import vehicle_type_dashboard
from ui.revenue import revenue_dashboard
from ui.cancellation import cancellation_dashboard
from ui.ratings import ratings_dashboard

# =====================================
# TITLE
# =====================================
st.title("🚖 OLA Ride Analytics Dashboard")

# =====================================
# DASHBOARD TABS
# =====================================
tabs = st.tabs([
    "Overall",
    "Vehicle Type",
    "Revenue",
    "Cancellation",
    "Ratings"
])

# =====================================
# LOAD DATA
# =====================================
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir,"OLA_Rides_Riview.csv")
    return pd.read_csv(file_path)
df = load_data()



# =====================================
# DATA CLEANUP (SAFE)
# =====================================
df = df.drop(columns=["vehicle_images", "unnamed_20"], errors="ignore")

# =====================================
# SIDEBAR (LOGO + FILTERS)
# =====================================
with st.sidebar:

    # ---- LOGO CARD ----
    st.markdown(
        """
        <div style="
            background-color:#020617;
            padding:16px;
            border-radius:12px;
            text-align:center;
            margin-bottom:12px;
        """,
        unsafe_allow_html=True
    )
    
  

    st.subheader("🔍 Filters")

    status_filter = st.multiselect(
        "Booking Status",
        options=df["booking_status"].dropna().unique(),
        default=df["booking_status"].dropna().unique(),
        key="status_filter"
    )

    vehicle_filter = st.multiselect(
        "Vehicle Type",
        options=df["vehicle_type"].dropna().unique(),
        default=df["vehicle_type"].dropna().unique(),
        key="vehicle_filter"
    )

    payment_filter = st.multiselect(
        "Payment Method",
        options=df["payment_method"].dropna().unique(),
        default=df["payment_method"].dropna().unique(),
        key="payment_filter"
    )

    st.subheader("⚙ Advanced Filters")

    rating_range = st.slider(
        "Customer Rating",
        0.0, 5.0, (0.0, 5.0), 0.5,
        key="rating_filter"
    )


# =====================================
# APPLY FILTERS (DEFINE filtered_df ONCE)
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

filtered_df = filtered_df[
    filtered_df["customer_rating"].between(
        rating_range[0], rating_range[1]
    )
]

# =====================================
# SEARCH BOOKING ID
# =====================================
search_id = st.text_input("🔎 Search Booking ID")

if search_id:
    filtered_df = filtered_df[
        filtered_df["booking_id"].astype(str).str.contains(search_id)
    ]

# =====================================
# KPI CALCULATIONS
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

cancellation_rate = round(
    (cancelled_rides / total_rides) * 100, 2
) if total_rides > 0 else 0.0

avg_customer_rating = round(
    filtered_df[
        (filtered_df["booking_status"] == "Success") &
        (filtered_df["incomplete_rides"] == "No")
    ]["customer_rating"].mean(),
    2
)

# =====================================
# TAB 1: OVERALL
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
        "Note: Successful bookings with incomplete rides are tracked separately."
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
# FOOTER
# =====================================
st.divider()
st.caption("Built with Streamlit • Python • Data sourced from cleaned CSV")
