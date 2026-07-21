import streamlit as st
import pandas as pd
import plotly.express as px
st.image("assets/logo.png", width=120)
st.set_page_config(page_title="Executive Report", layout="wide")

st.title("📑 Executive Business Report")

# ---------------- Load Dataset ----------------
df = pd.read_csv("customer_shopping_behavior.csv")

df.columns = df.columns.str.lower().str.replace(" ", "_")
df = df.rename(columns={"purchase_amount_(usd)": "purchase_amount"})

# ---------------- Business Summary ----------------

st.header("📌 Business Summary")

total_customers = len(df)
total_revenue = df["purchase_amount"].sum()
avg_purchase = df["purchase_amount"].mean()
avg_rating = df["review_rating"].mean()

c1, c2 = st.columns(2)
c3, c4 = st.columns(2)

c1.metric("👥 Customers", total_customers)
c2.metric("💰 Revenue", f"${total_revenue:,.0f}")
c3.metric("🛒 Avg Purchase", f"${avg_purchase:.2f}")
c4.metric("⭐ Avg Rating", f"{avg_rating:.2f}")

st.divider()

# ---------------- Summary Table ----------------

st.subheader("📊 Category Summary")

summary = df.groupby("category").agg(
    Revenue=("purchase_amount", "sum"),
    Customers=("purchase_amount", "count"),
    Average=("purchase_amount", "mean")
).reset_index()

st.dataframe(summary, use_container_width=True)

# ---------------- Revenue Chart ----------------

fig = px.bar(
    summary,
    x="category",
    y="Revenue",
    color="category",
    text_auto=True,
    title="Revenue by Category"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- Business Insights ----------------

st.header("📈 Business Insights")

top_category = summary.sort_values(
    "Revenue",
    ascending=False
).iloc[0]["category"]

top_payment = df["payment_method"].mode()[0]

top_season = (
    df.groupby("season")["purchase_amount"]
      .sum()
      .idxmax()
)

st.success(f"🏆 Highest Revenue Category: **{top_category}**")
st.info(f"💳 Most Used Payment Method: **{top_payment}**")
st.warning(f"🍂 Best Sales Season: **{top_season}**")

# ---------------- Top Customers ----------------

st.header("🏅 Top Customers")

top = df.nlargest(
    10,
    "purchase_amount"
)

cols = [
    c for c in [
        "customer_id",
        "gender",
        "category",
        "purchase_amount",
        "review_rating"
    ]
    if c in top.columns
]

st.dataframe(
    top[cols],
    use_container_width=True
)

# ---------------- Download ----------------

st.header("📥 Export")

csv = df.to_csv(index=False)

st.download_button(
    "⬇️ Download Full Dataset",
    csv,
    "customer_sales_report.csv",
    "text/csv"
)

st.divider()

st.markdown("""
## 📌 Final Project Features

✅ Multi-page Dashboard

✅ Interactive Filters

✅ KPI Cards

✅ Customer Insights

✅ Sales Analysis

✅ Payment Analysis

✅ Executive Report

✅ Download CSV

✅ Plotly Interactive Charts

✅ Streamlit Deployment

---
**Built using Python • Pandas • Plotly • Streamlit**
""")