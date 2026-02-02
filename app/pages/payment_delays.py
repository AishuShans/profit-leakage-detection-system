import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.set_page_config(page_title="Payment Delay Analysis", layout="wide")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    return pd.read_csv("data/processed/profit_leakage_cleaned.csv")

df = load_data()

# ---------------- PAGE TITLE ----------------
st.title("💳 Payment Delay Analysis")
st.write(
    """
    This module analyzes **delayed payments** and their impact on **profit leakage**.
    Identify customers or orders with **high outstanding amounts** and **late payments**.
    """
)

st.divider()

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔎 Payment Filters")

payment_delay_range = st.sidebar.slider(
    "Payment Delay (Days)",
    int(df["payment_delay_days"].min()),
    int(df["payment_delay_days"].max()),
    (int(df["payment_delay_days"].min()), int(df["payment_delay_days"].max()))
)

outstanding_range = st.sidebar.slider(
    "Outstanding Amount",
    float(df["outstanding_amount"].min()),
    float(df["outstanding_amount"].max()),
    (float(df["outstanding_amount"].min()), float(df["outstanding_amount"].max()))
)

# Optional filter by customer
customers = st.sidebar.multiselect(
    "Select Customers",
    options=df["customer_id"].unique(),
    default=df["customer_id"].unique()[:5]
)

# ---------------- APPLY FILTERS ----------------
filtered_df = df[
    (df["payment_delay_days"] >= payment_delay_range[0]) & (df["payment_delay_days"] <= payment_delay_range[1]) &
    (df["outstanding_amount"] >= outstanding_range[0]) & (df["outstanding_amount"] <= outstanding_range[1])
]

if customers:
    filtered_df = filtered_df[filtered_df["customer_id"].isin(customers)]

# ---------------- KPI METRICS ----------------
st.subheader("📊 Payment Delay KPIs")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", filtered_df["customer_id"].nunique())
col2.metric("Total Outstanding", f"₹ {filtered_df['outstanding_amount'].sum():,.0f}")
col3.metric("Avg Payment Delay", f"{filtered_df['payment_delay_days'].mean():.1f} days")
col4.metric("Max Payment Delay", f"{filtered_df['payment_delay_days'].max()} days")

st.divider()

# ---------------- VISUALIZATIONS ----------------
st.subheader("📈 Payment Patterns")

col1, col2 = st.columns(2)

# Payment Delay vs Outstanding Amount
with col1:
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.scatterplot(
        data=filtered_df,
        x="payment_delay_days",
        y="outstanding_amount",
        alpha=0.6,
        ax=ax
    )
    ax.set_title("Payment Delay vs Outstanding Amount")
    st.pyplot(fig)

# Histogram of Payment Delays
with col2:
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(filtered_df["payment_delay_days"], bins=30, kde=True, color="orange", ax=ax)
    ax.set_title("Payment Delay Distribution")
    st.pyplot(fig)

# ---------------- LEAKAGE IDENTIFICATION ----------------
st.subheader("🚨 Payment Delay Leakage Indicators")

# Define high risk: top 25% delays or outstanding
filtered_df["payment_risk_flag"] = np.where(
    (filtered_df["payment_delay_days"] > filtered_df["payment_delay_days"].quantile(0.75)) |
    (filtered_df["outstanding_amount"] > filtered_df["outstanding_amount"].quantile(0.75)),
    1, 0
)

risk_df = filtered_df[filtered_df["payment_risk_flag"] == 1]

st.write(f"⚠️ Potential Payment Delay Risk Records: **{len(risk_df)}**")

st.dataframe(
    risk_df[[
        "order_id",
        "customer_id",
        "outstanding_amount",
        "payment_delay_days"
    ]].head(10),
    use_container_width=True
)

st.divider()

# ---------------- BUSINESS INSIGHTS ----------------
st.subheader("📌 Business Insights")

st.markdown(
    """
    **Insights Identified:**
    - High payment delays impact cash flow and increase profit leakage risk
    - Certain customers or orders consistently delay payments
    - Large outstanding amounts amplify financial risk

    **Recommendations:**
    - Set automated alerts for overdue payments
    - Implement early payment incentives
    - Review credit terms for high-risk customers
    - Monitor top 25% delayed payments regularly
    """
)

# ---------------- FOOTER ----------------
st.markdown(
    """
    <div style="text-align:center; color:gray;">
        Profit Leakage Detection System • Payment Delay Module
    </div>
    """,
    unsafe_allow_html=True
)
