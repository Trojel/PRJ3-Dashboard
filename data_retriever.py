import requests
import pandas as pd
import streamlit as st


# Define the base URL of your Django API
base_url = 'http://127.0.0.1:8000//api/'

# Function to fetch data from the Django API
def fetch_sales_data(duration):
    url = f'http://127.0.0.1:8000/api/get_sales_data?duration={duration}'
    response = requests.get(url)
    
    if response.status_code == 200:
        sales_data = response.json()
        return pd.DataFrame(sales_data)
    else:
        st.error(f"Error fetching data: {response.status_code}")
        return pd.DataFrame()


# Function to fetch data from the Django API
def fetch_vendingmachine_data(id):
    url = f'http://127.0.0.1:8000/api/get_vendingmachines?organization_uuid={id}'
    response = requests.get(url)
    
    if response.status_code == 200:
        vendingMachine_json = response.json()
        vendingmachine_data = {item['UUID']: item['Vendingmachine Name '] for item in vendingMachine_json}
        return vendingmachine_data
        
    else:
        st.error(f"Error fetching data: {response.status_code}")


def fetch_product_leaderboard(duration, vendingmachine):
    url = f'http://127.0.0.1:8000/api/get_product_leaderboard?duration={duration}&vendingMachine_uuid={vendingmachine}'
    response = requests.get(url)
    
    if response.status_code == 200:
        vendingMachine_json = response.json()
        # Convert to a DataFrame
        df = pd.DataFrame(vendingMachine_json, columns=["Product", "Sales"])
        return df

        
    else:
        st.error(f"Error fetching product leaderboard data: {response.status_code}")


def fetch_inventory(vendingmachine, organization):
    url = f'http://127.0.0.1:8000/api/get_inventory?vendingMachine_uuid={vendingmachine}&organization_uuid={organization}'
    response = requests.get(url)

    if response.status_code == 200:
        inventory_json = response.json()
        #print(inventory_json)
        # Convert to a DataFrame
        df = pd.DataFrame(inventory_json, columns=["Product", "Remaining Quantity"])
        print(df)
        return df
    
def fetch_total_sales(duration: str, vendingMachine_uuid: str, organization_uuid: str):
    url = f'http://127.0.0.1:8000/api/get_total_sales?duration={duration}&vendingMachine_uuid={vendingMachine_uuid}&organization_uuid={organization_uuid}'
    response = requests.get(url)
    if response.status_code == 200:
        salesData = response.json()
        return salesData
    else:
        st.error(f"Error fetching total sales data: {response.status_code}")

def fetch_total_profits(duration: str, vendingMachine_uuid: str, organization_uuid: str):
    url = f'http://127.0.0.1:8000/api/get_total_profits?duration={duration}&vendingMachine_uuid={vendingMachine_uuid}&organization_uuid={organization_uuid}'
    response = requests.get(url)
    if response.status_code == 200:
        profitData = response.json()
        return profitData
        
    else:
        st.error(f"Error fetching total sales data: {response.status_code}")

def fetch_total_orders(duration: str, vendingMachine_uuid: str, organization_uuid: str):
    url = f'http://127.0.0.1:8000/api/total_orders?duration={duration}&vendingMachine_uuid={vendingMachine_uuid}&organization_uuid={organization_uuid}'
    response = requests.get(url)
    if response.status_code == 200:
        profitData = response.json()
        return profitData
        
    else:
        st.error(f"Error fetching total sales data: {response.status_code}")

        
    