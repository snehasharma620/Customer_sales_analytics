import streamlit as st

st.set_page_config(
    page_title="Customer Sales Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Customer Sales Analytics Dashboard")

st.markdown("""
## Welcome 👋

This dashboard provides interactive analytics on customer shopping behavior.

### Features

- 📈 Sales Analytics
- 👥 Customer Insights
- 💳 Payment Analysis
- 📊 Interactive Charts
- 📥 Download Reports

Select a page from the left sidebar.
""")

st.success("Dashboard Loaded Successfully ✅")