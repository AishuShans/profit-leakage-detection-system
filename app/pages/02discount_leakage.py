import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Discount Leakage Analysis", layout="wide")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    return pd.read_csv("data/processed/profit_leakage_cleaned.csv")

df = load_data()

# ---------------- PAGE TITLE ----------------
st.title("🏷️ Discount Leakage Analysis")
st.write(
    """
    This module analyzes how **discount strategies impact revenue and profit**.
    Excessive or poorly controlled discounts are one of the **primary causes of profit leakage**.
    """
)

st.divider()

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔎 Filter Discounts")

discount_range = st.sidebar.slider(
    "Discount Percentage",
    float(df["discount_percent"].min()),
    float(df["discount_percent"].max()),
    (
        float(df["discount_percent"].min()),
        float(df["discount_percent"].max())
    )
)

quantity_range = st.sidebar.slider(
    "Quantity Sold",
    int(df["quantity_sold"].min()),
    int(df["quantity_sold"].max()),
    (
        int(df["quantity_sold"].min()),
        int(df["quantity_sold"].max())
    )
)

margin_range = st.sidebar.slider(
    "Profit Margin (%)",
    float(df["profit_margin_percent"].min()),
    float(df["profit_margin_percent"].max()),
    (
        float(df["profit_margin_percent"].min()),
        float(df["profit_margin_percent"].max())
    )
)

# ---------------- APPLY FILTERS ----------------
filtered_df = df[
    (df["discount_percent"] >= discount_range[0]) &
    (df["discount_percent"] <= discount_range[1]) &
    (df["quantity_sold"] >= quantity_range[0]) &
    (df["quantity_sold"] <= quantity_range[1]) &
    (df["profit_margin_percent"] >= margin_range[0]) &
    (df["profit_margin_percent"] <= margin_range[1])
]

# ---------------- KPI METRICS ----------------
st.subheader("📊 Discount Impact Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Orders", len(filtered_df))
col2.metric("Avg Discount (%)", f"{filtered_df['discount_percent'].mean():.2f}")
col3.metric("Avg Profit Margin (%)", f"{filtered_df['profit_margin_percent'].mean():.2f}")
col4.metric("Total Discount Amount", f"₹ {filtered_df['discount_amount'].sum():,.0f}")

st.divider()

# ---------------- VISUALIZATIONS ----------------
st.subheader("📉 Discount Behavior Analysis")

col1, col2 = st.columns(2)

# Discount vs Quantity
with col1:
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.scatterplot(
        data=filtered_df,
        x="discount_percent",
        y="quantity_sold",
        alpha=0.6,
        ax=ax
    )
    ax.set_title("Discount vs Quantity Sold")
    st.pyplot(fig)

# Discount vs Profit Margin
with col2:
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.scatterplot(
        data=filtered_df,
        x="discount_percent",
        y="profit_margin_percent",
        alpha=0.6,
        ax=ax
    )
    ax.set_title("Discount vs Profit Margin")
    st.pyplot(fig)

st.divider()

# ---------------- LEAKAGE DETECTION ----------------
st.subheader("🚨 High Discount – Low Profit Orders")

leakage_df = filtered_df[
    (filtered_df["discount_percent"] > 30) &
    (filtered_df["profit_margin_percent"] < 5)
]

st.write(f"Orders with **high discount (>30%) & low profit (<5%)**: **{len(leakage_df)}**")

st.dataframe(
    leakage_df[
        [
            "order_id",
            "discount_percent",
            "discount_amount",
            "revenue",
            "profit_margin_percent"
        ]
    ].head(10),
    use_container_width=True
)

st.divider()

# ---------------- BUSINESS INSIGHTS ----------------
st.subheader("📌 Business Insights")

st.markdown(
    """
    **Key Insights from Discount Leakage Analysis:**
    - Higher discounts do not always result in higher quantity sold
    - Profit margins decline sharply beyond certain discount thresholds
    - Many transactions operate at near-zero margin due to aggressive discounting

    **Recommendations:**
    - Introduce discount caps based on margin sensitivity
    - Monitor discount effectiveness by product category
    - Replace flat discounts with volume-based pricing
    """
)

# ---------------- FOOTER ----------------
st.markdown(
    """
    <div style="text-align:center; color:gray;">
        Profit Leakage Detection System • Discount Leakage Module
    </div>
    """,
    unsafe_allow_html=True
)
