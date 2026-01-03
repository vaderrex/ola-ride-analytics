streamlit
pandas

# 🚖 OLA Ride Analytics Dashboard

An end-to-end data analytics project built using Python and Streamlit to analyze ride bookings, cancellations, and customer experience.

## 📌 Project Overview
This dashboard provides insights into ride demand, completion rates, cancellations, and customer ratings for OLA ride data.

## 🗂 Data Source
- Original dataset analyzed and cleaned using SQL Server (SSMS)
- Cleaned dataset exported to CSV for visualization

## 🧹 Data Handling
- Ratings available only for completed rides
- Cancelled and incomplete rides contain null ratings by design
- Presentation-level cleanup performed in Streamlit

## 📊 Features
- Dynamic filters (Booking Status, Vehicle Type, Payment Method)
- Key business KPIs
- Search by Booking ID
- Interactive data table

## 🛠 Tech Stack
- Python
- Pandas
- Streamlit
- SQL Server (for analysis phase)

## 🚀 How to Run
```bash
pip install -r requirements.txt
streamlit run app.py
