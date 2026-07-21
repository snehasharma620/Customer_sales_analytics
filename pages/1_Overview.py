import streamlit as st
import pandas as pd
import plotly.express as px
st.image("assets/logo.jpg", width=120)
st.set_page_config(page_title="Overview Dashboard", layout="wide")

st.title("📊 Customer Sales Analytics Dashboard")
st.caption("Overview Dashboard")

# ---------------- Load Dataset ----------------
df = pd.read_csv("customer_shopping_behavior.csv")

# Clean Column Names
df.columns = df.columns.str.lower().str.replace(" ", "_")
df = df.rename(columns={"purchase_amount_(usd)": "purchase_amount"})

# Age Group
labels = ["Young Adult", "Adult", "Middle-aged", "Senior"]
df["age_group"] = pd.qcut(df["age"], q=4, labels=labels)

# ---------------- Sidebar ----------------
st.sidebar.header("Filters")

gender = st.sidebar.multiselect(
    "Gender",
    options=df["gender"].unique(),
    default=df["gender"].unique()
)

category = st.sidebar.multiselect(
    "Category",
    options=df["category"].unique(),
    default=df["category"].unique()
)

season = st.sidebar.multiselect(
    "Season",
    options=df["season"].unique(),
    default=df["season"].unique()
)

subscription = st.sidebar.multiselect(
    "Subscription",
    options=df["subscription_status"].unique(),
    default=df["subscription_status"].unique()
)

filtered_df = df[
    (df["gender"].isin(gender)) &
    (df["category"].isin(category)) &
    (df["season"].isin(season)) &
    (df["subscription_status"].isin(subscription))
]

# ---------------- KPI Cards ----------------
st.subheader("Key Performance Indicators")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Customers", len(filtered_df))
c2.metric("Revenue ($)", f"{filtered_df['purchase_amount'].sum():,.0f}")
c3.metric("Average Purchase", f"{filtered_df['purchase_amount'].mean():.2f}")
c4.metric("Average Rating", f"{filtered_df['review_rating'].mean():.2f}")

st.divider()

# ---------------- Charts ----------------

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
        filtered_df.groupby("category")["purchase_amount"].sum().reset_index(),
        x="category",
        y="purchase_amount",
        color="category",
        title="Revenue by Category"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.pie(
        filtered_df,
        names="subscription_status",
        hole=0.5,
        title="Subscription Status"
    )
    st.plotly_chart(fig, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    fig = px.bar(
        filtered_df.groupby("gender")["purchase_amount"].sum().reset_index(),
        x="gender",
        y="purchase_amount",
        color="gender",
        title="Revenue by Gender"
    )
    st.plotly_chart(fig, use_container_width=True)

with col4:
    fig = px.bar(
        filtered_df.groupby("season")["purchase_amount"].sum().reset_index(),
        x="season",
        y="purchase_amount",
        color="season",
        title="Season-wise Revenue"
    )
    st.plotly_chart(fig, use_container_width=True)

col5, col6 = st.columns(2)

with col5:
    fig = px.pie(
        filtered_df,
        names="payment_method",
        hole=0.45,
        title="Payment Method Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

with col6:
    fig = px.histogram(
        filtered_df,
        x="purchase_amount",
        color="gender",
        nbins=25,
        title="Purchase Amount Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------- Download ----------------
st.subheader("Download Data")

st.download_button(
    "📥 Download Filtered Dataset",
    filtered_df.to_csv(index=False),
    "filtered_customer_data.csv",
    "text/csv"
)

# ---------------- Data ----------------
st.subheader("Dataset Preview")

st.dataframe(filtered_df, use_container_width=True)

st.markdown("---")
st.markdown("### Built using Python • Pandas • Plotly • Streamlit")