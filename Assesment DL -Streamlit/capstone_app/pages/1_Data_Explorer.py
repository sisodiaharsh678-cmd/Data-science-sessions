import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Data Explorer", layout="wide")
st.title("📊 Data Explorer")


uploaded_file = st.file_uploader("Upload Delivery CSV File", type=["csv"])

if uploaded_file is None:
    st.info(
        "Please upload a delivery data CSV file to view summary statistics "
        "and charts. Expected columns: hour, city, restaurant, "
        "delivery_time_minutes, revenue."
    )
else:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Could not read the uploaded file: {e}")
        st.stop()

    required_cols = ["hour", "restaurant", "delivery_time_minutes", "revenue"]
    missing_cols = [col for col in required_cols if col not in df.columns]

    if missing_cols:
        st.error(
            f"Uploaded CSV is missing required columns: {missing_cols}. "
            "Please check your file and try again."
        )
    else:
        # ---------------------------------------------------------
        # Summary statistics
        # ---------------------------------------------------------
        total_orders = len(df)
        avg_delivery_time = df["delivery_time_minutes"].mean()
        total_revenue = df["revenue"].sum()

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Orders", f"{total_orders}")
        col2.metric("Avg Delivery Time", f"{avg_delivery_time:.1f} mins")
        col3.metric("Total Revenue", f"₹{total_revenue:,.2f}")

        st.divider()

        #Hourly Order Volume Trend
        st.subheader("Hourly Order Volume Trend")

        hourly_orders = (
            df.groupby("hour")
            .size()
            .reset_index(name="order_count")
            .sort_values("hour")
        )

        fig_hourly = px.line(
            hourly_orders,
            x="hour",
            y="order_count",
            markers=True,
            title="Orders by Hour of Day"
        )
        fig_hourly.update_layout(xaxis_title="Hour of Day", yaxis_title="Order Count")
        st.plotly_chart(fig_hourly, use_container_width=True)

        #Delivery Time Distribution by Restaurant
        st.subheader("Delivery Time Distribution by Restaurant")

        fig_dist = px.box(
            df,
            x="restaurant",
            y="delivery_time_minutes",
            title="Delivery Time Spread per Restaurant",
            points="outliers"
        )
        fig_dist.update_layout(
            xaxis_title="Restaurant", yaxis_title="Delivery Time (mins)"
        )
        st.plotly_chart(fig_dist, use_container_width=True)
