import streamlit as st
import pandas as pd

# --- Load logo from URL ---
st.image("https://luxvers.com/wp-content/uploads/2023/06/logo-luxvers-bianco.png", width=200)

# --- Page title ---
st.title("Luxvers Supplier Order Tracking Dashboard")

# --- Load order data ---
@st.cache_data
def load_data():
    return pd.read_csv("luxvers_order_tracking_cleaned.csv")

df = load_data()

# --- Filters ---
with st.sidebar:
    st.header("Filter Orders")
    client_ids = df["CLIENT ID"].dropna().unique()
    selected_clients = st.multiselect("Select Client ID(s)", client_ids, default=client_ids)
    pickup_status = st.multiselect("Pick Up Status", df["Pick Up Status (Done / Not Done)"].dropna().unique())
    transfer_status = st.multiselect("Transfer Activated", df["Transfer Activated (Yes / No)"].dropna().unique())

# --- Filtered data ---
filtered_df = df[
    (df["CLIENT ID"].isin(selected_clients)) &
    (df["Pick Up Status (Done / Not Done)"].isin(pickup_status) if pickup_status else True) &
    (df["Transfer Activated (Yes / No)"].isin(transfer_status) if transfer_status else True)
]

# --- Show dashboard table ---
st.subheader("📦 Order Overview")
st.dataframe(filtered_df, use_container_width=True)

# --- Status Highlights ---
st.subheader("✅ Order Status Summary")

def status_summary(column):
    return filtered_df[column].value_counts().to_frame().rename(columns={column: "Count"})

for col in [
    "Transfer Activated (Yes / No)",
    "Documents Created (Invoice and Packing List)",
    "Payment Received (Yes / No)",
    "MRN Created (Yes / No)",
    "Pick Up Status (Done / Not Done)"
]:
    st.write(f"**{col}**")
    st.dataframe(status_summary(col))

# --- Download Button ---
st.download_button(
    label="📥 Download Filtered Orders",
    data=filtered_df.to_csv(index=False).encode('utf-8'),
    file_name='luxvers_filtered_orders.csv',
    mime='text/csv'
)
