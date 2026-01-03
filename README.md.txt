# 🚖 OLA Ride Analytics – End-to-End Data Analytics Project

## 📌 Business Objective
Analyze ride booking data to understand demand patterns, cancellations,
revenue distribution, and service quality to support data-driven decisions.

## 📊 Data Source
- Raw ride booking data (CSV/XLSX)
- Cleaned using Python (Pandas)
- Stored in SQL Server for analysis

## 🧹 Data Cleaning & Assumptions
- Ratings are available only for successfully completed rides
- Cancelled and incomplete rides have null ratings by design
- Excel artifacts and unused columns were removed at the presentation layer

## 🗄️ SQL Analysis
- Performed exploratory and aggregation queries using SQL Server (SSMS)
- Queries include revenue analysis, cancellation reasons, and ride metrics

## 📈 Tableau Dashboard
- Interactive KPIs and visualizations
- Focused on ride volume, vehicle performance, and customer satisfaction

## 🌐 Streamlit Web Application
- Built using Python and Streamlit
- Live filters for booking status, vehicle type, and payment method
- Dynamic KPIs reflecting user-selected filters

## 🔑 Key Insights
- Majority of revenue comes from digital payment methods
- Cancellations are driven mainly by customer-related issues
- Higher-rated vehicle types show better ride completion rates

## 🛠️ Tech Stack
- Python (Pandas, Streamlit)
- SQL Server
- Tableau
- GitHub

## 📸 Screenshots
![Streamlit Dashboard](screenshots/streamlit_dashboard.png)
![Tableau Dashboard](screenshots/tableau_dashboard.png)
