import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Profit Leakage Detection System",
    layout="wide"
)

# ---------------- TITLE ----------------
st.markdown(
    """
    <h1 style="text-align:center; color:#2c3e50;">
        💰 Profit Leakage Detection System
    </h1>
    <h4 style="text-align:center; color:#7f8c8d;">
        Analytics Dashboard (EDA • Statistics • Visualization)
    </h4>
    """,
    unsafe_allow_html=True
)

st.write("")
st.write("")

# ---------------- ABOUT ----------------
st.subheader("📌 About This Project")

st.markdown(
    """
    This dashboard presents a **comprehensive Profit Leakage Detection System**
    built using **realistic business transaction data**.

    The objective is to **identify hidden revenue losses** caused by:
    - Inefficient pricing
    - Excessive discounts
    - Product returns and refunds
    - Inventory mismanagement
    - Delayed customer payments

    The project focuses on:
    - Data preprocessing  
    - Normalization & standardization  
    - Exploratory Data Analysis (EDA)  
    - Business-driven visual analytics  

    🚫 **No machine learning models are used** — this is a **pure analytics project**.
    """
)

st.divider()

# ---------------- DATA OVERVIEW ----------------
st.subheader("📊 Dataset Coverage")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("📦 **Sales & Revenue**\n\nPricing, Cost, Profit Margins")

with col2:
    st.info("🏷️ **Discounts & Returns**\n\nDiscount % , Refund Amount")

with col3:
    st.info("🚚 **Operations & Payments**\n\nInventory, Supplier Delay, Payment Delay")

st.divider()

# ---------------- MODULES ----------------
st.subheader("🧩 Leakage Analysis Modules")

col1, col2, col3 = st.columns(3)

with col1:
    st.success("**1️⃣ Revenue & Profit Leakage**\n\nPricing gaps and margin erosion")

with col2:
    st.success("**2️⃣ Discount Leakage**\n\nExcessive discount impact")

with col3:
    st.success("**3️⃣ Returns & Refunds**\n\nRevenue loss due to returns")

st.write("")

col4, col5 = st.columns(2)

with col4:
    st.success("**4️⃣ Inventory Leakage**\n\nOverstock & understock analysis")

with col5:
    st.success("**5️⃣ Payment Delay Leakage**\n\nOutstanding revenue risk")

st.divider()

# ---------------- NAVIGATION ----------------
st.subheader("🚀 Navigate to Analysis Pages")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("📈 Revenue & Profit"):
        st.switch_page("pages/revenue_profit.py")

with col2:
    if st.button("🏷️ Discounts"):
        st.switch_page("pages/discount_leakage.py")

with col3:
    if st.button("↩️ Returns"):
        st.switch_page("pages/returns_refunds.py")

with col4:
    if st.button("📦 Inventory"):
        st.switch_page("pages/inventory_leakage.py")

with col5:
    if st.button("💳 Payments"):
        st.switch_page("pages/payment_delays.py")

st.divider()

# ---------------- FOOTER ----------------
st.markdown(
    """
    <div style="text-align:center; color:gray;">
        Built with Python • Pandas • Seaborn • Matplotlib • Streamlit  
        <br>
        Profit Leakage Detection System
    </div>
    """,
    unsafe_allow_html=True
)
