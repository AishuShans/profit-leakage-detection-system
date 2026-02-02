import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Revenue & Profit Leakage", layout="wide")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    return pd.read_csv("data/processed/profit_leakage_cleaned.csv")

df = load_data()

# ---------------- PAGE TITLE ----------------
st.title("📉 Revenue & Profit Leakage Analysis")
st.write(
    """
    This module analyzes **revenue, cost, and profit margin patterns**
    to identify **hidden profit leakage** caused by pricing gaps,
    discounts, and cost inefficiencies.
    """
)

st.divider()

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔎 Filter Transactions")

# Quantity filter
qty_range = st.sidebar.slider(
    "Quantity Sold",
    int(df["quantity_sold"].min()),
    int(df["quantity_sold"].max()),
    (int(df["quantity_sold"].min()), int(df["quantity_sold"].max()))
)

# Profit margin filter
margin_range = st.sidebar.slider(
    "Profit Margin (%)",
    float(df["profit_margin_percent"].min()),
    float(df["profit_margin_percent"].max()),
    (
        float(df["profit_margin_percent"].min()),
        float(df["profit_margin_percent"].max())
    )
)

# Discount filter
discount_range = st.sidebar.slider(
    "Discount (%)",
    float(df["discount_percent"].min()),
    float(df["discount_percent"].max()),
    (
        float(df["discount_percent"].min()),
        float(df["discount_percent"].max())
    )
)

# Revenue filter
revenue_range = st.sidebar.slider(
    "Revenue Range",
    float(df["revenue"].min()),
    float(df["revenue"].max()),
    (
        float(df["revenue"].min()),
        float(df["revenue"].max())
    )
)

# ---------------- APPLY FILTERS ----------------
filtered_df = df[
    (df["quantity_sold"] >= qty_range[0]) &
    (df["quantity_sold"] <= qty_range[1]) &
    (df["profit_margin_percent"] >= margin_range[0]) &
    (df["profit_margin_percent"] <= margin_range[1]) &
    (df["discount_percent"] >= discount_range[0]) &
    (df["discount_percent"] <= discount_range[1]) &
    (df["revenue"] >= revenue_range[0]) &
    (df["revenue"] <= revenue_range[1])
]

st.subheader("📊 Filtered Dataset Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Orders", len(filtered_df))
col2.metric("Total Revenue", f"₹ {filtered_df['revenue'].sum():,.0f}")
col3.metric("Total Cost", f"₹ {filtered_df['cost'].sum():,.0f}")
col4.metric("Avg Profit Margin (%)", f"{filtered_df['profit_margin_percent'].mean():.2f}")

st.divider()

# ---------------- VISUALIZATIONS ----------------
st.subheader("📈 Revenue & Profit Insights")

col1, col2 = st.columns(2)

# Revenue vs Cost
with col1:
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.scatterplot(
        data=filtered_df,
        x="revenue",
        y="cost",
        alpha=0.5,
        ax=ax
    )
    ax.set_title("Revenue vs Cost")
    st.pyplot(fig)

# Profit Margin Distribution
with col2:
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(
        filtered_df["profit_margin_percent"],
        bins=30,
        kde=True,
        ax=ax
    )
    ax.set_title("Profit Margin Distribution")
    st.pyplot(fig)

st.divider()

# ---------------- LEAKAGE IDENTIFICATION ----------------
st.subheader("🚨 High-Risk Profit Leakage Orders")

leakage_df = filtered_df[filtered_df["profit_margin_percent"] < 5]

st.write(
    f"Orders with **profit margin < 5%**: **{len(leakage_df)}**"
)

st.dataframe(
    leakage_df[
        [
            "order_id",
            "revenue",
            "cost",
            "discount_percent",
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
    **Key observations from Revenue & Profit Leakage Analysis:**

    - High revenue does **not guarantee profitability**
    - Excessive discounts significantly erode margins
    - Cost-heavy orders contribute to hidden losses
    - Low-margin transactions are prime leakage sources

    **Actionable Recommendations:**
    - Review pricing strategy for low-margin orders
    - Set discount thresholds based on margin impact
    - Optimize cost structure for bulk orders
    """
)

# ---------------- FOOTER ----------------
st.markdown(
    """
    <div style="text-align:center; color:gray;">
        Profit Leakage Detection System • Revenue & Profit Module
    </div>
    """,
    unsafe_allow_html=True
)
