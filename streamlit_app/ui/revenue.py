import streamlit as st

def revenue_dashboard(df):
    st.markdown("## 💳 Revenue Analysis")
    st.caption("Revenue performance by payment method and vehicle type")
    st.divider()

    # ---------------------------------
    # Business-correct revenue base
    # ---------------------------------
    revenue_df = df[
        (df["booking_status"] == "Success") &
        (df["incomplete_rides"] == "No")
    ]

    total_revenue = revenue_df["booking_value"].sum()
    avg_revenue_per_ride = round(revenue_df["booking_value"].mean(), 1)
    total_revenue_rides = revenue_df.shape[0]

    # ---------------------------------
    # KPI Row
    # ---------------------------------
    c1, c2, c3 = st.columns(3)

    c1.metric("Total Revenue (₹)", f"{total_revenue:,.0f}")
    c2.metric("Avg Revenue per Ride (₹)", f"{avg_revenue_per_ride:,.1f}")
    c3.metric("Revenue-Generating Rides", total_revenue_rides)

    st.write("")

    # ---------------------------------
    # Charts
    # ---------------------------------
    st.markdown("### 💳 Revenue Distribution")
    left, right = st.columns(2)

    with left:
        st.markdown("**Revenue by Payment Method**")
        revenue_by_payment = (
            revenue_df
            .groupby("payment_method")["booking_value"]
            .sum()
            .sort_values(ascending=False)
        )
        st.bar_chart(revenue_by_payment)

    with right:
        st.markdown("**Revenue by Vehicle Type**")
        revenue_by_vehicle = (
            revenue_df
            .groupby("vehicle_type")["booking_value"]
            .sum()
            .sort_values(ascending=False)
        )
        st.bar_chart(revenue_by_vehicle)
