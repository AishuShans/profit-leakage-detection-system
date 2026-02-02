import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Inventory Leakage Analysis", layout="wide")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    return pd.read_csv("data/processed/profit_leakage_cleaned.csv")

df = load_data()

# ---------------- PAGE TITLE ----------------
st.title("📦 Inventory Leakage Analysis")
st.write(
    """
    This module analyzes **inventory inefficiencies** that cause profit leakage,
    including **overstocking, understocking, holding cost, and supplier delays**.
    """
)

st.divider()

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔎 Inventory Filters")

inventory_range = st.sidebar.slider(
    "Inventory Level",
    int(df["inventory_level"].min()),
    int(df["inventory_level"].max()),
    (
        int(df["inventory_level"].min()),
        int(df["inventory_level"].max())
    )
)

holding_cost_range = st.sidebar.slider(
    "Holding Cost",
    float(df["holding_cost"].min()),
    float(df["holding_cost"].max()),
    (
        float(df["holding_cost"].min()),
        float(df["holding_cost"].max())
    )
)

supplier_delay_range = st.sidebar.slider(
    "Supplier Delay (Days)",
    int(df["supplier_delay_days"].min()),
    int(df["supplier_delay_days"].max()),
    (
        int(df["supplier_delay_days"].min()),
        int(df["supplier_delay_days"].max())
    )
)

# ---------------- APPLY FILTERS ----------------
filtered_df = df[
    (df["inventory_level"] >= inventory_range[0]) &
    (df["inventory_level"] <= inventory_range[1]) &
    (df["holding_cost"] >= holding_cost_range[0]) &
    (df["holding_cost"] <= holding_cost_range[1]) &
    (df["supplier_delay_days"] >= supplier_delay_range[0]) &
    (df["supplier_delay_days"] <= supplier_delay_range[1])
]

# ---------------- KPI METRICS ----------------
st.subheader("📊 Inventory KPIs")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Products", filtered_df["product_id"].nunique())
col2.metric("Avg Inventory Level", int(filtered_df["inventory_level"].mean()))
col3.metric("Avg Holding Cost", f"₹ {filtered_df['holding_cost'].mean():,.0f}")
col4.metric("Avg Supplier Delay", f"{filtered_df['supplier_delay_days'].mean():.1f} days")

st.divider()

# ---------------- VISUALIZATIONS ----------------
st.subheader("📉 Inventory Risk Patterns")

col1, col2 = st.columns(2)

# Inventory vs Holding Cost
with col1:
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.scatterplot(
        data=filtered_df,
        x="inventory_level",
        y="holding_cost",
        alpha=0.6,
        ax=ax
    )
    ax.set_title("Inventory Level vs Holding Cost")
    st.pyplot(fig)

# Supplier Delay vs Inventory
with col2:
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.scatterplot(
        data=filtered_df,
        x="supplier_delay_days",
        y="inventory_level",
        alpha=0.6,
        ax=ax
    )
    ax.set_title("Supplier Delay vs Inventory Level")
    st.pyplot(fig)

st.divider()

# ---------------- LEAKAGE IDENTIFICATION ----------------
st.subheader("🚨 Inventory Leakage Indicators")

leakage_df = filtered_df[
    (filtered_df["inventory_level"] > filtered_df["reorder_level"] * 2) |
    (filtered_df["holding_cost"] > filtered_df["holding_cost"].quantile(0.75))
]

st.write(f"⚠️ Potential Inventory Leakage Records: **{len(leakage_df)}**")

st.dataframe(
    leakage_df[
        [
            "product_id",
            "inventory_level",
            "reorder_level",
            "holding_cost",
            "supplier_delay_days"
        ]
    ].head(10),
    use_container_width=True
)

st.divider()

# ---------------- BUSINESS INSIGHTS ----------------
st.subheader("📌 Business Insights")

st.markdown(
    """
    **Insights Identified:**
    - Overstocking significantly increases holding cost
    - Supplier delays force excess buffer inventory
    - Poor reorder thresholds amplify leakage risk

    **Recommendations:**
    - Optimize reorder levels using demand trends
    - Penalize chronic supplier delays
    - Introduce inventory aging analysis
    """
)

# ---------------- FOOTER ----------------
st.markdown(
    """
    <div style="text-align:center; color:gray;">
        Profit Leakage Detection System • Inventory Leakage Module
    </div>
    """,
    unsafe_allow_html=True
)
