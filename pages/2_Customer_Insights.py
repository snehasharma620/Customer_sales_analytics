import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Customer Insights",
    page_icon="👥",
    layout="wide"
)

# ---------------- LOGO ----------------
st.image("assets/logo.jpg", width=120)

st.title("👥 Customer Insights Dashboard")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("customer_shopping_behavior.csv")

df.columns = df.columns.str.lower().str.replace(" ", "_")
df = df.rename(columns={"purchase_amount_(usd)": "purchase_amount"})

# ---------------- FIX DATA ----------------
df["review_rating"] = pd.to_numeric(
    df["review_rating"],
    errors="coerce"
)

df["purchase_amount"] = pd.to_numeric(
    df["purchase_amount"],
    errors="coerce"
)

df["previous_purchases"] = pd.to_numeric(
    df["previous_purchases"],
    errors="coerce"
)

df["review_rating"] = df["review_rating"].fillna(1)
df["purchase_amount"] = df["purchase_amount"].fillna(0)
df["previous_purchases"] = df["previous_purchases"].fillna(0)

labels = [
    "Young Adult",
    "Adult",
    "Middle-aged",
    "Senior"
]

df["age_group"] = pd.qcut(
    df["age"],
    q=4,
    labels=labels
)

# ---------------- SIDEBAR ----------------
st.sidebar.title("📊 Customer Analytics")

gender = st.sidebar.multiselect(
    "Gender",
    options=df["gender"].unique(),
    default=df["gender"].unique()
)

age_group = st.sidebar.multiselect(
    "Age Group",
    options=df["age_group"].unique(),
    default=df["age_group"].unique()
)

filtered = df[
    (df["gender"].isin(gender))
    &
    (df["age_group"].isin(age_group))
].copy()

# ---------------- KPI ----------------
c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Customers",
    len(filtered)
)

c2.metric(
    "Average Age",
    round(filtered["age"].mean(),1)
)

c3.metric(
    "Average Rating",
    round(filtered["review_rating"].mean(),2)
)

c4.metric(
    "Previous Purchases",
    int(filtered["previous_purchases"].sum())
)

st.divider()

# ---------------- ROW 1 ----------------

col1,col2 = st.columns(2)

with col1:

    fig = px.histogram(
        filtered,
        x="age",
        color="gender",
        nbins=20,
        title="Age Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    fig = px.pie(
        filtered,
        names="gender",
        hole=.5,
        title="Gender Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ---------------- ROW 2 ----------------

col3,col4 = st.columns(2)

with col3:
    scatter_df = filtered.copy()

    scatter_df["review_rating"] = (pd.to_numeric(scatter_df["review_rating"], errors="coerce")
    .fillna(1))
    fig = px.scatter(
        filtered,
        x="age",
        y="purchase_amount",
        color="gender",
        hover_data=["review_rating"],
        size_max=18,
        title="Age vs Purchase Amount"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
with col4:

    fig = px.box(
        filtered,
        x="gender",
        y="purchase_amount",
        color="gender",
        title="Purchase Distribution by Gender"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ---------------- Revenue by Age Group ----------------

st.subheader("💰 Revenue by Age Group")

age_revenue = (
    filtered.groupby("age_group", observed=False)["purchase_amount"]
    .sum()
    .reset_index()
)

fig = px.bar(
    age_revenue,
    x="age_group",
    y="purchase_amount",
    color="age_group",
    text_auto=True,
    title="Revenue by Age Group"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- Customer Segmentation ----------------

st.subheader("👥 Customer Segmentation")

filtered["Customer Segment"] = pd.cut(
    filtered["purchase_amount"],
    bins=[0, 50, 150, 1000],
    labels=["Low Value", "Medium Value", "High Value"]
)

fig = px.pie(
    filtered,
    names="Customer Segment",
    title="Customer Segments"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- Top Customers ----------------

if "customer_id" in filtered.columns:

    st.subheader("🏆 Top 10 Customers")

    top = filtered.nlargest(10, "purchase_amount")

    st.dataframe(
        top[
            [
                "customer_id",
                "age",
                "gender",
                "category",
                "purchase_amount",
                "review_rating",
            ]
        ],
        use_container_width=True,
    )

# ---------------- Rating Distribution ----------------

fig = px.histogram(
    filtered,
    x="review_rating",
    color="gender",
    nbins=10,
    title="Customer Review Rating Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- Dataset ----------------

st.subheader("📋 Customer Dataset")

st.dataframe(filtered, use_container_width=True)

st.download_button(
    "📥 Download Customer Data",
    filtered.to_csv(index=False),
    "customer_insights.csv",
    "text/csv",
)

st.markdown("---")
st.caption(
    "Built with ❤️ using Python • Streamlit • Pandas • Plotly"
)