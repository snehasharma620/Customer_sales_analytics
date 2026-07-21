import streamlit as st
import pandas as pd
import plotly.express as px
st.image("assets/logo.png", width=120)
st.set_page_config(page_title="Payment Analysis", layout="wide")

st.title("💳 Payment Analysis Dashboard")

# ---------------- Load Dataset ----------------

df = pd.read_csv("customer_shopping_behavior.csv")

df.columns = df.columns.str.lower().str.replace(" ", "_")
df = df.rename(columns={"purchase_amount_(usd)": "purchase_amount"})

# ---------------- Sidebar ----------------

st.sidebar.header("Filters")

payment = st.sidebar.multiselect(
    "Payment Method",
    df["payment_method"].unique(),
    default=df["payment_method"].unique()
)

subscription = st.sidebar.multiselect(
    "Subscription Status",
    df["subscription_status"].unique(),
    default=df["subscription_status"].unique()
)

gender = st.sidebar.multiselect(
    "Gender",
    df["gender"].unique(),
    default=df["gender"].unique()
)

filtered = df[
    (df["payment_method"].isin(payment)) &
    (df["subscription_status"].isin(subscription)) &
    (df["gender"].isin(gender))
]

# ---------------- KPI Cards ----------------

c1,c2,c3,c4 = st.columns(4)

c1.metric("Transactions", len(filtered))
c2.metric("Revenue", f"${filtered.purchase_amount.sum():,.0f}")
c3.metric("Avg Transaction", f"${filtered.purchase_amount.mean():.2f}")
c4.metric("Avg Rating", round(filtered.review_rating.mean(),2))

st.divider()

# ---------------- Charts ----------------

col1,col2 = st.columns(2)

with col1:

    fig = px.pie(
        filtered,
        names="payment_method",
        hole=0.5,
        title="Payment Method Distribution"
    )

    st.plotly_chart(fig,use_container_width=True)

with col2:

    fig = px.bar(
        filtered.groupby("payment_method")["purchase_amount"].sum().reset_index(),
        x="payment_method",
        y="purchase_amount",
        color="payment_method",
        text_auto=True,
        title="Revenue by Payment Method"
    )

    st.plotly_chart(fig,use_container_width=True)

# ---------------- Row 2 ----------------

col3,col4 = st.columns(2)

with col3:

    fig = px.box(
        filtered,
        x="payment_method",
        y="purchase_amount",
        color="payment_method",
        title="Purchase Distribution"
    )

    st.plotly_chart(fig,use_container_width=True)

with col4:

    fig = px.bar(
        filtered.groupby("payment_method")["review_rating"].mean().reset_index(),
        x="payment_method",
        y="review_rating",
        color="payment_method",
        text_auto=True,
        title="Average Rating"
    )

    st.plotly_chart(fig,use_container_width=True)

# ---------------- Previous Purchases ----------------

st.subheader("Previous Purchases")

fig = px.histogram(
    filtered,
    x="previous_purchases",
    color="payment_method",
    nbins=20
)

st.plotly_chart(fig,use_container_width=True)

# ---------------- Revenue Table ----------------

st.subheader("Payment Summary")

summary = filtered.groupby("payment_method").agg(

Revenue=("purchase_amount","sum"),
Transactions=("purchase_amount","count"),
Average=("purchase_amount","mean")

).reset_index()

st.dataframe(summary,use_container_width=True)

# ---------------- Download ----------------

st.download_button(

"📥 Download Payment Report",

summary.to_csv(index=False),

"payment_report.csv",

"text/csv"

)

st.markdown("---")

st.markdown("### Payment Analysis Dashboard")