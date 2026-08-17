import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="Hourly Order Analytics", layout="wide")
st.title("Hourly Order Counts by Restaurant")


uploaded_file = st.file_uploader("Upload hourly orders CSV", type=["csv"])

if uploaded_file is None:
    st.info("Upload a CSV with columns: hour, restaurant, order_count")
else:
    df = pd.read_csv(uploaded_file)

    fig = px.line(
        df,
        x="hour",
        y="order_count",
        color="restaurant",
        markers=True,
        title="Hourly Order Volume by Restaurant"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "Zoom by click-dragging over the chart, hover for exact values, "
        "and click a restaurant name in the legend to toggle it on/off."
    )

