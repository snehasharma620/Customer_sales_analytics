import streamlit as st
import pandas as pd
import plotly.express as px
st.image("assets/logo.jpg", width=120)
st.set_page_config(page_title="Sales Analysis", layout="wide")

st.title("📈 Sales Analysis Dashboard")

# ---------------- Load Data ----------------
df = pd.read_csv("customer_shopping_behavior.csv")

df.columns = df.columns.str.lower().str.replace(" ", "_")
df = df.rename(columns={"purchase_amount_(usd)": "purchase_amount"})

# ---------------- Sidebar ----------------
st.sidebar.title("📊 Customer Analytics")
st.sidebar.success("Interactive Dashboard")
st.sidebar.header("Sales Filters")

category = st.sidebar.multiselect(
    "Category",
    df["category"].unique(),
    default=df["category"].unique()
)

season = st.sidebar.multiselect(
    "Season",
    df["season"].unique(),
    default=df["season"].unique()
)

shipping = st.sidebar.multiselect(
    "Shipping Type",
    df["shipping_type"].unique(),
    default=df["shipping_type"].unique()
)

filtered = df[
    (df["category"].isin(category)) &
    (df["season"].isin(season)) &
    (df["shipping_type"].isin(shipping))
]

# ---------------- KPI Cards ----------------

c1,c2,c3,c4 = st.columns(4)

c1.metric("Total Revenue", f"${filtered.purchase_amount.sum():,.0f}")
c2.metric("Orders", len(filtered))
c3.metric("Average Order Value", f"${filtered.purchase_amount.mean():.2f}")
c4.metric("Highest Sale", f"${filtered.purchase_amount.max():.2f}")

st.divider()

# ---------------- Revenue by Category ----------------

col1,col2 = st.columns(2)

with col1:

    fig = px.bar(
        filtered.groupby("category")["purchase_amount"].sum().reset_index(),
        x="category",
        y="purchase_amount",
        color="category",
        text_auto=True,
        title="Revenue by Category"
    )

    st.plotly_chart(fig,use_container_width=True)

with col2:

    fig = px.bar(
        filtered.groupby("season")["purchase_amount"].sum().reset_index(),
        x="season",
        y="purchase_amount",
        color="season",
        text_auto=True,
        title="Season-wise Revenue"
    )

    st.plotly_chart(fig,use_container_width=True)

# ---------------- Shipping Analysis ----------------

col3,col4 = st.columns(2)

with col3:

    fig = px.bar(
        filtered.groupby("shipping_type")["purchase_amount"].sum().reset_index(),
        x="shipping_type",
        y="purchase_amount",
        color="shipping_type",
        text_auto=True,
        title="Revenue by Shipping Type"
    )

    st.plotly_chart(fig,use_container_width=True)

with col4:

    fig = px.pie(
        filtered,
        names="category",
        hole=0.5,
        title="Sales Share by Category"
    )

    st.plotly_chart(fig,use_container_width=True)

# ---------------- Histogram ----------------

st.subheader("Purchase Amount Distribution")

fig = px.histogram(
    filtered,
    x="purchase_amount",
    color="category",
    nbins=30
)

st.plotly_chart(fig,use_container_width=True)

# ---------------- Top Categories ----------------

st.subheader("Top Categories")

top = filtered.groupby("category")["purchase_amount"].sum().reset_index()

top = top.sort_values(
    by="purchase_amount",
    ascending=False
)

st.dataframe(top,use_container_width=True)

# ---------------- Raw Data ----------------

st.subheader("Sales Dataset")

st.dataframe(filtered,use_container_width=True)

st.download_button(
    "📥 Download Sales Data",
    filtered.to_csv(index=False),
    "sales_analysis.csv",
    "text/csv"
)

st.markdown("---")
st.markdown("### Sales Analysis | Python • Pandas • Plotly • Streamlit")