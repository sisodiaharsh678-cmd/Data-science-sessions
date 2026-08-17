import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(
    page_title="Online Sales Dashboard",
    layout="wide"
)

st.title("Online Sales Analytics Dashboard")

upload_file = st.file_uploader("Upload Here", type=["csv"])

if upload_file is not None:
    df = pd.read_csv(upload_file)

    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)


#################### FILTERS ######################

    st.sidebar.header("filter")

    Region_filter = st.sidebar.multiselect(
        "Region",
        options = df["Region"].unique(),
        default = df["Region"].unique()
    )

    Category_filter = st.sidebar.multiselect(
        "Product Category",
        options = df["Product Category"].unique(),
        default = df["Product Category"].unique()
    )

    date_range = st.sidebar.date_input(
        "Date Range",
        [df["Date"].min(), df["Date"].max() ]
    )

    search_product = st.sidebar.text_input(
        "Search pRODUCT name"
    )

    filtered_df = df[
    (df["Product Category"].isin(Category_filter)) &
    (df["Region"].isin(Region_filter))&
    (df["Date"].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])))
    ]


    if search_product:
        filtered_df = filtered_df[
            filtered_df["Product Name"]
            .str.contains(search_product, case=False)
    ]
        
    total_revenue = filtered_df["Total Revenue"].sum()
    avg_units = filtered_df["Units Sold"].mean()
    avg_price = filtered_df["Unit Price"].mean()

    kpi1, kpi2, kpi3 = st.columns(3)

    kpi1.metric("Total_Revenue",total_revenue)
    kpi2.metric("Unit SOLD", int(avg_units))
    kpi3.metric("Unit price", int(avg_price))



    col1, col2 = st.columns(2)

    with col1:
        st.subheader("revenue by product category")
        fig_bar = px.bar(
            filtered_df,
            x= "Product Category",
            y="Total Revenue",
            color = "Product Category",
            text_auto= True
        )
        st.plotly_chart(fig_bar, use_container_width=True) 

    with col2:
        st.subheader(" Revenue Trend Over Time (Plotly)")
        trend_df = (
            filtered_df.groupby("Date")["Total Revenue"]
            .sum()
            .reset_index()
        )
        fig_line = px.line(
            trend_df,
            x="Date",
            y="Total Revenue",
            markers=True
        )
        st.plotly_chart(fig_line, use_container_width=True)


    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Revenue by Region")
        fig_pie = px.pie(
            filtered_df,
            names="Region",
            values="Total Revenue"
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col4:
        st.subheader("Price vs Units Sold")
        fig_scatter = px.scatter(
            filtered_df,
            x="Unit Price",
            y="Units Sold",
            size="Total Revenue",
            color="Product Category",
            hover_data=["Product Name"]
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    
    col5, col6 = st.columns(2)

    with col5:
        st.subheader("Unit Price Distribution (Matplotlib)")
        fig, ax = plt.subplots()
        ax.hist(filtered_df["Unit Price"], bins=20)
        ax.set_xlabel("Unit Price")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

    with col6:
        st.subheader("Revenue Distribution by Category (Seaborn)")
        fig, ax = plt.subplots()
        sns.boxplot(
            data=filtered_df,
            x="Product Category",
            y="Total Revenue",
            ax=ax
        )
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

    with st.expander("View Filtered Data"):
        st.dataframe(filtered_df)

        csv = filtered_df.to_csv(index=False).encode()
        st.download_button(
            "Download Filtered Data",
            csv,
            "filtered_online_sales.csv",
            "text/csv"
        )

else:
    st.info("Please upload Online Sales Data CSV file")