import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Food Delivery Analysis", 
    page_icon=":bar_chart:", 
    layout="wide"
)

@st.cache_data
def load_data():
    try:
        return pd.read_csv(r"food_delivery_10_years_cleaned.csv")  # Using relative path
    except FileNotFoundError:
        st.error("Error: Data file not found! Please ensure 'food_delivery_10_years_cleaned.csv' is in the same directory.")
        return None
    except Exception as e:
        st.error(f"An error occurred while loading the data: {str(e)}")
        return None

df1 = load_data()
if df1 is None:
    st.stop()

st.sidebar.title("Filters")
year_filter = st.sidebar.selectbox(
    "Select Year", 
    df1['order_year'].unique(), 
    key="year"
)
month_filter = st.sidebar.selectbox(
    "Select Month", 
    df1['order_month'].unique(), 
    key="month"
)
day_filter = st.sidebar.selectbox(
    "Select Day", 
    df1['order_day'].unique(), 
    key="day"
)

filtered_df = df1[
    (df1['order_year'] == year_filter) &
    (df1['order_month'] == month_filter) &
    (df1['order_day'] == day_filter)
].copy()

st.title("Food Delivery Analysis Dashboard")
st.subheader("Exploring Food Delivery Data")

st.write("""
This dashboard provides insights into food delivery data over a period of 10 years.
The dataset contains information about orders, delivery times, and discounts offered.
""")

st.write("### Data Overview")
st.write(f"Dataset shape: Rows: {filtered_df.shape[0]}, Columns: {filtered_df.shape[1]}")
st.write("Columns:", filtered_df.columns.tolist())

with st.expander("View Sample Data"):
    st.write(filtered_df.head())

with st.expander("View Data Description"):
    st.write(filtered_df.describe(include='all'))

with st.expander("View Data Types"):
    st.write(filtered_df.dtypes)

with st.expander("View Unique Values"):
    st.write(filtered_df.nunique())

st.write("### Data Distribution")

col1, col2 = st.columns(2)
with col1:
    st.write("#### Order Time Distribution")
    st.bar_chart(filtered_df['order_hour'].value_counts(), use_container_width=True)

with col2:
    st.write("#### Delivery Time Distribution")
    st.bar_chart(filtered_df['delivery_hour'].value_counts(), use_container_width=True)

st.write("#### Discounts and Offers Distribution")
st.bar_chart(filtered_df['discounts_and_offers'].value_counts(), use_container_width=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Sales Analysis", "Customer Behavior", "Financial Metrics", "Order Dates", "Delivery Dates"])

with tab1:
    st.header("Sales Performance")
    
    col1, col2 = st.columns(2)
    with col1:
        # Monthly Order Value
        monthly_sales = filtered_df.groupby('order_month')['order_value'].sum().reset_index()
        fig = px.bar(monthly_sales, x='order_month', y='order_value', 
                     title='Total Order Value by Month', color='order_value')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Orders by Day of Week
        daily_orders = filtered_df['order_day'].value_counts().reset_index()
        fig = px.bar(daily_orders, x='order_day', y='count', 
                     title='Orders by Day of Week', color='count')
        st.plotly_chart(fig, use_container_width=True)
    
    # Hourly Order Pattern
    hourly_orders = filtered_df['order_hour'].value_counts().sort_index().reset_index()
    fig = px.line(hourly_orders, x='order_hour', y='count', 
                 title='Orders by Hour of Day', markers=True)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Customer Behavior")
    
    col1, col2 = st.columns(2)
    with col1:
        payment_data = filtered_df['payment_method'].value_counts().reset_index()
        fig = px.pie(payment_data, values='count', names='payment_method', 
                    title='Payment Method Distribution')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        discount_data = filtered_df['discount_source'].value_counts().reset_index()
        fig = px.pie(discount_data, values='count', names='discount_source', 
                    title='Discount Source Distribution')
        st.plotly_chart(fig, use_container_width=True)
    
    fig = px.scatter(filtered_df, x='discount_value', y='order_value',
                    title='Impact of Discounts on Order Value',
                    trendline='ols')
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Financial Metrics")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Delivery Fees", f"${filtered_df['delivery_fee'].sum():,.2f}")
    
    with col2:
        st.metric("Total Commission Fees", f"${filtered_df['commission_fee'].sum():,.2f}")
    
    filtered_df['commission_percentage'] = (filtered_df['commission_fee'] / filtered_df['order_value']) * 100
    fig = px.box(filtered_df, y='commission_percentage', 
                title='Commission Percentage Distribution')
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.write("##### Order Date Distribution")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.bar_chart(filtered_df['order_year'].value_counts())
    with col2:
        st.bar_chart(filtered_df['order_month'].value_counts())
    with col3:
        st.bar_chart(filtered_df['order_day'].value_counts())

with tab5:
    st.write("##### Delivery Date Distribution")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.bar_chart(filtered_df['delivery_year'].value_counts())
    with col2:
        st.bar_chart(filtered_df['delivery_month'].value_counts())
    with col3:
        st.bar_chart(filtered_df['delivery_day'].value_counts())
