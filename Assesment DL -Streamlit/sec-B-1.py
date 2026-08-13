import streamlit as st
import pandas as pd 
 

st.set_page_config(page_title="Delivery Summary Dashboard", layout="wide")
st.title(" Delivery Summary Dashboard")
 

uploaded_file = st.file_uploader("Upload Delivery CSV File", type=["csv"])
 
if uploaded_file is None:
    st.info("Please upload a delivery data CSV file to see the dashboard.")
else:
    
    df = pd.read_csv(uploaded_file)
 
    
    required_cols = ["city", "delivery_time_minutes", "revenue", "restaurant"]
    missing_cols = [col for col in required_cols if col not in df.columns]
 
    if missing_cols:
        st.error(f"Uploaded CSV is missing required columns: {missing_cols}")
    else:
        
        cities = sorted(df["city"].unique())
        selected_city = st.sidebar.selectbox("Select City", cities)
 
        
        filtered_df = df[df["city"] == selected_city]
 
        
        total_orders = len(filtered_df)
        avg_delivery_time = filtered_df["delivery_time_minutes"].mean()
        total_revenue = filtered_df["revenue"].sum()
 
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Orders", f"{total_orders}")
        col2.metric("Avg Delivery Time", f"{avg_delivery_time:.1f} mins")
        col3.metric("Total Revenue", f"₹{total_revenue:,.2f}")
 
        st.divider()
 
        
        st.subheader(f"Orders per Restaurant — {selected_city}")
 
        orders_per_restaurant = (
            filtered_df.groupby("restaurant")
            .size()
            .reset_index(name="order_count")
            .set_index("restaurant")
        )
 
        st.bar_chart(orders_per_restaurant["order_count"])