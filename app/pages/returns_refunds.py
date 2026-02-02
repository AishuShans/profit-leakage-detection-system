import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.set_page_config(page_title="Returns & Refunds Analysis", layout="wide")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    return pd.read_csv("data/processed/profit_leakage_cleaned.csv")

df = load_data()

# ---------------- PAGE TITLE ----------------
st.title("🔄 Returns & Refunds Analysis")
st.write(
    """
    This module analyzes **returned orders and refund amounts** to identify areas
    where profit is leaking due to product returns or incorrect transactions.
    """
)

st.divider()

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔎 Refund Filters")

refund_range = st.sidebar.slider(
    "Refund Amount",
    float(df["refund_amount"].min()),
    float(df["refund_amount"].max()),
    (float(df["refund_amount"].min()), float(df["refund_amount"].max()))
)

return_quantity_range = st.sidebar.slider(
    "Quantity Returned",
    int(df["quantity_sold"].min()),
    int(df["quantity_sold"].max()),
    (int(df["quantity_sold"].min()), int(df["quantity_sold"].max()))
)

customers = st.sidebar.multiselect(
    "Select Customers",
    options=df["customer_id"].unique(),
    default=df["customer_id"].unique()[:5]
)

products = st.sidebar.multiselect(
    "Select Products",
    options=df["product_id"].unique(),
    default=df["product_id"].unique()[:5]
)

# ---------------- APPLY FILTERS ----------------
filtered_df = df[
    (df["refund_amount"] >= refund_range[0]) & (df["refund_amount"] <= refund_range[1]) &
    (df["quantity_sold"] >= return_quantity_range[0]) & (df["quantity_sold"] <= return_quantity_range[1])
]

if customers:
    filtered_df = filtered_df[filtered_df["customer_id"].isin(customers)]

if products:
    filtered_df = filtered_df[filtered_df["product_id"].isin(products)]

# ---------------- KPI METRICS ----------------
st.subheader("📊 Returns & Refund KPIs")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Orders Returned", filtered_df.shape[0])
col2.metric("Total Refund Amount", f"₹ {filtered_df['refund_amount'].sum():,.0f}")
col3.metric("Avg Refund Amount", f"₹ {filtered_df['refund_amount'].mean():,.0f}")
col4.metric("Max Refund Amount", f"₹ {filtered_df['refund_amount'].max():,.0f}")

st.divider()

# ---------------- VISUALIZATIONS ----------------
st.subheader("📈 Returns & Refund Patterns")

col1, col2 = st.columns(2)

# Refund Amount vs Quantity Returned
with col1:
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.scatterplot(
        data=filtered_df,
        x="quantity_sold",
        y="refund_amount",
        alpha=0.6,
        ax=ax
    )
    ax.set_title("Quantity Returned vs Refund Amount")
    st.pyplot(fig)

# Histogram of Refund Amount
with col2:
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(filtered_df["refund_amount"], bins=30, kde=True, color="red", ax=ax)
    ax.set_title("Refund Amount Distribution")
    st.pyplot(fig)

# ---------------- LEAKAGE IDENTIFICATION ----------------
st.subheader("🚨 Refund & Returns Leakage Indicators")

# Flag high-risk refunds: top 25% by refund amount or return quantity
filtered_df["return_risk_flag"] = np.where(
    (filtered_df["refund_amount"] > filtered_df["refund_amount"].quantile(0.75)) |
    (filtered_df["quantity_sold"] > filtered_df["quantity_sold"].quantile(0.75)),
    1, 0
)

risk_df = filtered_df[filtered_df["return_risk_flag"] == 1]

st.write(f"⚠️ Potential Return & Refund Risk Records: **{len(risk_df)}**")

st.dataframe(
    risk_df[[
        "order_id",
        "customer_id",
        "product_id",
        "quantity_sold",
        "refund_amount"
    ]].head(10),
    use_container_width=True
)

st.divider()

# ---------------- BUSINESS INSIGHTS ----------------
st.subheader("📌 Business Insights")

st.markdown(
    """
    **Insights Identified:**
    - High refund amounts or return quantities indicate potential profit leakage
    - Certain products or customers contribute disproportionately to losses
    - Frequent returns increase operational cost and inventory risk

    **Recommendations:**
    - Review refund and return policies for high-risk products
    - Track customers with repeated high-value returns
    - Introduce quality checks and better order verification
    - Monitor top 25% refund amounts regularly
    """
)

# ---------------- FOOTER ----------------
st.markdown(
    """
    <div style="text-align:center; color:gray;">
        Profit Leakage Detection System • Returns & Refunds Module
    </div>
    """,
    unsafe_allow_html=True
)
