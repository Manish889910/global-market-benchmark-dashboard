import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Global Market Benchmark Dashboard",
    page_icon="📊",
    layout="wide"
)

# -----------------------------------
# LOAD DATA
# -----------------------------------
data = pd.read_csv("global_ecommerce_sales.csv")
data.columns = data.columns.str.strip()
data["Order_Date"] = pd.to_datetime(data["Order_Date"])

# -----------------------------------
# SIDEBAR FILTERS
# -----------------------------------
st.sidebar.header("🔎 Filter Data")

selected_country = st.sidebar.multiselect(
    "Select Country",
    options=data["Country"].unique(),
    default=data["Country"].unique()
)

selected_category = st.sidebar.multiselect(
    "Select Category",
    options=data["Category"].unique(),
    default=data["Category"].unique()
)

# -----------------------------------
# CURRENCY SELECTOR
# -----------------------------------
st.sidebar.markdown("### 💱 Select Currency")

currency_option = st.sidebar.selectbox(
    "Choose Currency",
    ["USD", "EUR", "INR", "GBP", "RUB"]
)

# USD Base Conversion Rates
conversion_rates = {
    "USD": 1,
    "EUR": 0.92,
    "INR": 83,
    "GBP": 0.79,
    "RUB": 92
}

currency_symbols = {
    "USD": "$",
    "EUR": "€",
    "INR": "₹",
    "GBP": "£",
    "RUB": "₽"
}

rate = conversion_rates[currency_option]
symbol = currency_symbols[currency_option]

# -----------------------------------
# FILTER DATA
# -----------------------------------
filtered_data = data[
    (data["Country"].isin(selected_country)) &
    (data["Category"].isin(selected_category))
]

# -----------------------------------
# NUMBER FORMAT FUNCTION (NO TRUNCATION)
# -----------------------------------
def format_large_number(value, symbol):
    abs_value = abs(value)

    if abs_value >= 1_000_000_000:
        formatted = f"{abs_value/1_000_000_000:.2f}B"
    elif abs_value >= 1_000_000:
        formatted = f"{abs_value/1_000_000:.2f}M"
    elif abs_value >= 1_000:
        formatted = f"{abs_value/1_000:.2f}K"
    else:
        formatted = f"{abs_value:,.2f}"

    return f"{symbol}{formatted}"

# -----------------------------------
# HEADER BANNER
# -----------------------------------
st.markdown("""
    <div style='background-color:#0E2F44;padding:20px;border-radius:10px'>
        <h1 style='color:white;text-align:center;'>
        Global Market Benchmarking Dashboard
        </h1>
        <p style='color:white;text-align:center;'>
        Data-Driven Framework for International Market Expansion Decision
        </p>
    </div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

# -----------------------------------
# KPI SECTION
# -----------------------------------
st.subheader("📈 Key Performance Indicators")

total_revenue = filtered_data["Total_Amount"].sum() * rate
total_orders = filtered_data["Order_ID"].nunique()
average_order_value = filtered_data["Total_Amount"].mean() * rate
total_quantity = filtered_data["Quantity"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", format_large_number(total_revenue, symbol))
col2.metric("Total Orders", total_orders)
col3.metric("Avg Order Value", format_large_number(average_order_value, symbol))
col4.metric("Units Sold", f"{total_quantity:,}")

st.caption(f"All financial values displayed in {currency_option} (Base dataset in USD)")

st.markdown("---")

# -----------------------------------
# REVENUE BY CATEGORY
# -----------------------------------
colA, colB = st.columns(2)

with colA:
    st.subheader("📊 Revenue by Category")
    category_revenue = filtered_data.groupby("Category")["Total_Amount"].sum() * rate

    fig1, ax1 = plt.subplots()
    ax1.bar(category_revenue.index, category_revenue.values)
    plt.xticks(rotation=45)
    st.pyplot(fig1)

with colB:
    st.subheader("🌍 Revenue by Country")
    country_revenue = filtered_data.groupby("Country")["Total_Amount"].sum() * rate

    fig2, ax2 = plt.subplots()
    ax2.bar(country_revenue.index, country_revenue.values)
    plt.xticks(rotation=45)
    st.pyplot(fig2)

st.markdown("---")

# -----------------------------------
# MONTHLY TREND
# -----------------------------------
st.subheader("📅 Monthly Revenue Trend")

filtered_data["Month"] = filtered_data["Order_Date"].dt.to_period("M")
monthly_revenue = filtered_data.groupby("Month")["Total_Amount"].sum() * rate

fig3, ax3 = plt.subplots()
ax3.plot(monthly_revenue.index.astype(str), monthly_revenue.values, marker="o")
plt.xticks(rotation=45)
st.pyplot(fig3)

st.markdown("---")

# -----------------------------------
# STRATEGIC INSIGHT BLOCK
# -----------------------------------
st.markdown("""
    <div style='background-color:#0E2F44;padding:20px;border-radius:10px'>
        <h3 style='color:white;'>🎯 Strategic Insight</h3>
        <p style='color:white;'>
        Global revenue benchmarking indicates strong demand concentration 
        in high-performing product categories and digitally mature economies. 
        These comparative patterns support structured evaluation of future 
        international market expansion opportunities.
        </p>
    </div>
""", unsafe_allow_html=True)

st.write("")

# -----------------------------------
# METHODOLOGICAL NOTE BLOCK
# -----------------------------------
st.markdown("""
    <div style='background-color:#1F4E79;padding:15px;border-radius:8px'>
        <h4 style='color:white;'>📘 Methodological Note</h4>
        <p style='color:white; font-size:14px;'>
        The dataset represents global e-commerce sales excluding Russia. 
        Therefore, the market entry evaluation is derived using cross-country 
        demand benchmarking and macro-environmental analysis rather than 
        direct Russian transactional data.
        </p>
    </div>
""", unsafe_allow_html=True)