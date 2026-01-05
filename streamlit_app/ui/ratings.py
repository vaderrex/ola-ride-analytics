import streamlit as st
import pandas as pd

def ratings_dashboard(df):
    # =================================================
    # Header
    # =================================================
    st.markdown("## 🟢 Ratings Analysis")
    st.caption("Customer and driver satisfaction for completed rides")
    st.divider()

    # =================================================
    # Identify rating columns safely
    # =================================================
    customer_rating_col = None
    driver_rating_col = None

    for col in df.columns:
        col_lower = col.lower()
        if "customer" in col_lower and "rating" in col_lower:
            customer_rating_col = col
        if "driver" in col_lower and "rating" in col_lower:
            driver_rating_col = col

    if customer_rating_col is None or driver_rating_col is None:
        st.error("❌ Rating columns not found in the dataset.")
        st.write("Available columns:", df.columns.tolist())
        return

    # =================================================
    # Business-correct ratings base
    # =================================================
    ratings_df = df[
        (df["booking_status"] == "Success") &
        (df["incomplete_rides"] == "No")
    ]

    if ratings_df.empty:
        st.info(
            "ℹ️ **No completed rides with ratings found for the selected filters.**\n\n"
            "Try adjusting Booking Status or Vehicle Type filters."
        )
        return

    # =================================================
    # KPIs
    # =================================================
    avg_customer_rating = round(
        ratings_df[customer_rating_col].mean(), 2
    )

    avg_driver_rating = round(
        ratings_df[driver_rating_col].mean(), 2
    )

    rated_rides = ratings_df.shape[0]

    k1, k2, k3 = st.columns(3)
    k1.metric("Avg Customer Rating", avg_customer_rating)
    k2.metric("Avg Driver Rating", avg_driver_rating)
    k3.metric("Rated Completed Rides", rated_rides)

    st.write("")

    # =================================================
    # Rating Distribution
    # =================================================
    st.markdown("### 📊 Rating Distribution")

    left, right = st.columns(2)

    with left:
        st.markdown("**Customer Rating Distribution**")
        st.bar_chart(
            ratings_df[customer_rating_col]
            .value_counts()
            .sort_index()
        )

    with right:
        st.markdown("**Driver Rating Distribution**")
        st.bar_chart(
            ratings_df[driver_rating_col]
            .value_counts()
            .sort_index()
        )

    # =================================================
    # Ratings by Vehicle Type
    # =================================================
    st.markdown("### 🚗 Ratings by Vehicle Type")

    vehicle_ratings = (
        ratings_df
        .groupby("vehicle_type")[[customer_rating_col, driver_rating_col]]
        .mean()
        .round(2)
        .sort_values(customer_rating_col, ascending=False)
    )

    st.dataframe(
        vehicle_ratings,
        use_container_width=True
    )

    # =================================================
    # Customer vs Driver Insight
    # =================================================
    rating_gap = round(
        avg_customer_rating - avg_driver_rating, 2
    )

    if rating_gap > 0:
        insight = (
            "📌 **Insight:** Customers rate rides slightly higher than drivers, "
            "indicating generally positive ride experiences with some driver-side concerns."
        )
    elif rating_gap < 0:
        insight = (
            "📌 **Insight:** Drivers rate rides higher than customers, "
            "suggesting potential gaps in customer experience."
        )
    else:
        insight = (
            "📌 **Insight:** Customer and driver ratings are well aligned, "
            "indicating balanced satisfaction."
        )

    st.success(insight)
