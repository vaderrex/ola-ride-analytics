import streamlit as st
import pandas as pd


def vehicle_type_dashboard(df):
    st.markdown("## 🚖 Vehicle Type Analysis")
    st.caption("Usage patterns and distance distribution by vehicle category")
    st.divider()

    total_vehicle_types = df["vehicle_type"].nunique()
    most_used_vehicle = df["vehicle_type"].value_counts().idxmax()
    avg_distance = round(df["ride_distance"].mean(), 1)

    c1, c2, c3 = st.columns(3)
    c1.metric("Vehicle Categories", total_vehicle_types)
    c2.metric("Most Used Vehicle", most_used_vehicle)
    c3.metric("Avg Ride Distance (km)", f"{avg_distance}")

    st.write("")

    st.markdown("### 📈 Ride Distribution")
    left, right = st.columns(2)

    with left:
        st.markdown("**Top 5 Vehicle Types by Rides**")
        st.bar_chart(
            df["vehicle_type"]
            .value_counts()
            .head(5)
        )

    with right:
        st.markdown("**Average Ride Distance by Vehicle Type**")
        st.bar_chart(
            df.groupby("vehicle_type")["ride_distance"]
            .mean()
            .sort_values(ascending=False)
        )
