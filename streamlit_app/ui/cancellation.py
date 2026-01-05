import streamlit as st
import pandas as pd

def cancellation_dashboard(df):
    # =================================================
    # Header
    # =================================================
    st.markdown("## ⚠️ Cancellation Analysis")
    st.caption("Cancellation volume, responsibility, and failure reasons")
    st.divider()

    # =================================================
    # Identify cancellation reason columns safely
    # =================================================
    customer_col = None
    driver_col = None

    for col in df.columns:
        col_lower = col.lower()
        if "customer" in col_lower and "cancel" in col_lower:
            customer_col = col
        if "driver" in col_lower and "cancel" in col_lower:
            driver_col = col

    if customer_col is None or driver_col is None:
        st.error("⚠️ Cancellation reason columns not found in the dataset.")
        st.write("Available columns:", df.columns.tolist())
        return

    # =================================================
    # Cancellation base (BUSINESS-CORRECT)
    # =================================================
    cancelled_df = df[
        df["booking_status"].str.contains(
            "Cancelled|Driver Not Found",
            case=False,
            na=False
        )
    ]

    # -------------------------------------------------
    # UX: Empty state
    # -------------------------------------------------
    if cancelled_df.empty:
        st.info(
            "ℹ️ **No cancelled or failed rides found for the selected filters.**\n\n"
            "Try adjusting **Booking Status**, **Vehicle Type**, or **Payment Method** "
            "from the filters on the left."
        )
        return

    # =================================================
    # KPI calculations
    # =================================================
    total_rides = df.shape[0]
    total_cancelled = cancelled_df.shape[0]

    cancellation_rate = (
        round((total_cancelled / total_rides) * 100, 2)
        if total_rides > 0 else 0.0
    )

    customer_cancelled = cancelled_df[customer_col].notna().sum()
    driver_cancelled = cancelled_df[driver_col].notna().sum()

    system_failures = cancelled_df[
        cancelled_df["booking_status"]
        .str.contains("Driver Not Found", case=False, na=False)
    ].shape[0]

    # =================================================
    # KPI Row
    # =================================================
    k1, k2, k3, k4 = st.columns(4)

    k1.metric("Total Rides", total_rides)
    k2.metric("Failed / Cancelled Rides", total_cancelled)
    k3.metric("Cancellation Rate (%)", cancellation_rate)
    k4.metric("System Failures", system_failures)

    st.write("")

    # =================================================
    # Responsibility & Failure Analysis
    # =================================================
    st.markdown("### 📈 Cancellation Responsibility & Failure Analysis")
    st.caption(
        "Human-initiated cancellations are shown separately from "
        "system-level failures (e.g., Driver Not Found)."
    )

    r1, r2, r3 = st.columns(3)

    r1.metric("Customer Cancellations", customer_cancelled)
    r2.metric("Driver Cancellations", driver_cancelled)
    r3.metric("System-Level Failures", system_failures)

    st.info(
        "ℹ️ Most failed bookings under the selected filters are caused by "
        "**system-level issues** rather than direct customer or driver cancellations."
    )

    # =================================================
    # Top Cancellation & Failure Reasons
    # =================================================
    st.markdown("### 🧾 Top Cancellation & Failure Reasons")
    st.caption(
        "Most frequent reasons across customer, driver, and system-level failures"
    )

    reasons = (
        pd.concat([
            cancelled_df[customer_col],
            cancelled_df[driver_col]
        ])
        .dropna()
        .value_counts()
        .head(7)
    )

    st.bar_chart(reasons)

    st.success(
        "📌 **Insight:** Improving driver availability and system reliability will "
        "have a greater impact on reducing cancellations than focusing only on "
        "customer behavior."
    )

    # =================================================
    # Detail Table
    # =================================================
    st.divider()
    st.markdown("### 📄 Cancelled & Failed Ride Details")

    st.dataframe(
        cancelled_df[
            [
                "booking_id",
                "booking_status",
                "vehicle_type",
                "payment_method",
                customer_col,
                driver_col
            ]
        ],
        use_container_width=True
    )
