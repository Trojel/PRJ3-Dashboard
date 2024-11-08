import pandas as pd
import requests
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards
import streamlit as st
from data_retriever import *  # Assuming you have functions to fetch data

# Default settings
st.set_page_config(layout="wide", page_title="Vending Machine Dashboard", page_icon="🍺")
primaryColor = '#7d13e8'

# Get the organisation from the URL
organisation = st.query_params["organisation"]
st.write(f"Organisation: {organisation}")

# Set the title of the dashboard
st.title('Vending Machine Dashboard')

# Create a 3-column layout
col1, col2, col3 = st.columns([0.2, 0.5, 0.2])

# Initialize session state for caching data
if 'data_updated' not in st.session_state:
    st.session_state.data_updated = False

# Fetch data function
def refresh_data():
    st.session_state.data_updated = True


# Select time duration
with col1:
    with st.container(border=True):
        duration = st.selectbox('Select Time Period:', ['today', 'last_week', 'last_month', 'last_3_months', 'last_6_months', 'last_year'])

        # Fetch the vending machine data
        vendingmachine_data = fetch_vendingmachine_data(organisation)
        vendingmachine_data["All Vendingmachines"] = "All Vendingmachines"

        # Create the dropdown list with Streamlit
        def format_func(chosen_vendingmachine):
            return vendingmachine_data[chosen_vendingmachine]

        chosen_vendingmachine = st.selectbox("Select option", options=list(vendingmachine_data.keys()), format_func=format_func)

        # Button to refresh data
        if st.button('Refresh Data'):
         refresh_data()  # Update session state

# Refresh data based on button click
if st.session_state.data_updated:
    # Metrics
    with col1:
        with st.container(border=True):
            st.subheader('Sales Overview')

            # Use st.metric with dynamic percentage
            salesData = fetch_total_sales(duration, chosen_vendingmachine, organisation)
            st.metric(label="Total Sales", value=salesData['Total Sales'], delta=f"{salesData['Percentage Change']}%")
            profitData = fetch_total_profits(duration, chosen_vendingmachine, organisation)
            st.metric(label="Total Profits", value=profitData['Total Profit'], delta=f"{profitData['Percentage Change']}%")

            orderData = fetch_total_orders(duration, chosen_vendingmachine, organisation)
            st.metric(label="Total Orders", value=orderData['Total Orders'], delta=orderData['Percentage Change'])
            style_metric_cards(border_left_color=primaryColor)

    # Sales per Day
    with col2:
        with st.container(border=True):
            st.subheader('Sales per Day')

            # Call the API and get the data
            df_sales = fetch_sales_data(duration)

            if not df_sales.empty:
                # Convert sale_date to a datetime format for grouping if necessary
                df_sales['datetime'] = pd.to_datetime(df_sales['datetime'])

                # Group by sale_date and sum the amount (or any other relevant aggregation)
                sales_summary = df_sales.groupby('datetime')['value'].sum().reset_index()

                # Display the data in a bar chart
                st.bar_chart(sales_summary.set_index('datetime'), color='#7d13e8', height=300)
            else:
                st.write("No sales data available for the selected period.")

            # Product Leaderboard
            with st.container(border=True):
                st.subheader('Product Leaderboard')
                # Create a horizontal bar chart using Plotly
                fig = px.bar(
                    fetch_product_leaderboard(duration, chosen_vendingmachine),
                    x='Sales',
                    y='Product',
                    orientation='h',  # 'h' for horizontal bars
                    color_discrete_sequence=['#7d13e8'],  # Set bar color
                    color_continuous_scale="Viridis"
                )

                # Update layout to make it look nice
                fig.update_layout(
                    height=300,
                    title="Sales per Product",
                    xaxis_title="Sales Quantity",
                    yaxis_title="Product",
                    showlegend=False,
                )

                # Display the Plotly chart in Streamlit
                st.plotly_chart(fig)

# Product inventory
with col3:
    with st.container(border=True):
        st.subheader('Product inventory')
        st.bar_chart(fetch_inventory(chosen_vendingmachine, organisation).set_index('Product'), horizontal=True, height=300, color='#7d13e8')
