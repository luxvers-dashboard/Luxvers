import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# --- Logo ---
st.image("https://luxvers.com/wp-content/uploads/2023/06/logo-luxvers-bianco.png", width=200)

# --- Title ---
st.title("Luxvers Supplier Order Tracking Dashboard")

# --- Load data from Google Sheet CSV export ---
google_sheet_url = "https://docs.google.com/spreadsheets/d/15SNQ1QaaU1VNK-nlWnuILPHfbdWqOjW-/export?format=csv"

def load_data():
    return pd.read_csv(google_sheet_url)

# Refresh button
if st.button("🔄 Refresh Data from Google Sheet"):
    st.session_state.df = load_data()

# Initial load (or fallback)
if "df" not in st.session_state:
    st.session_state.df = load_data()

df = st.session_state.df

# --- Filters ---
with st.sidebar:
    st.header("🔎 Filter Orders")
    client_ids = df["CLIENT ID"].dropna().unique()
    selected_clients = st.multiselect("Select Client ID(s)", client_ids, default=client_ids)
    pickup_status = st.multiselect("Pick Up Status", df["Pick Up Status (Done / Not Done)"].dropna().unique())
    transfer_status = st.multiselect("Transfer Activated", df["Transfer Activated (Yes / No)"].dropna().unique())

# --- Apply filters ---
filtered_df = df[
    (df["CLIENT ID"].isin(selected_clients)) &
    (df["Pick Up Status (Done / Not Done)"].isin(pickup_status) if pickup_status else True) &
    (df["Transfer Activated (Yes / No)"].isin(transfer_status) if transfer_status else True)
]

# --- Display filtered data ---
st.subheader("📦 Filtered Order Data")
st.dataframe(filtered_df, use_container_width=True)

# --- Charts ---
st.subheader("📊 Order Status Charts")

col1, col2 = st.columns(2)

with col1:
    if "Quantity Sent" in filtered_df.columns and "Quantity Confirmed" in filtered_df.columns:
        fig, ax = plt.subplots()
        ax.bar(filtered_df["CLIENT ID"].astype(str), filtered_df["Quantity Sent"], label="Sent", alpha=0.7)
        ax.bar(filtered_df["CLIENT ID"].astype(str), filtered_df["Quantity Confirmed"], label="Confirmed", alpha=0.7)
        ax.set_ylabel("Quantity")
        ax.set_title("Sent vs Confirmed")
        ax.legend()
        st.pyplot(fig)

with col2:
    if "Transfer Activated (Yes / No)" in filtered_df.columns:
        transfer_counts = filtered_df["Transfer Activated (Yes / No)"].value_counts()
        st.write("**Transfer Status**")
        st.bar_chart(transfer_counts)

# --- File Upload ---
st.subheader("📤 Upload Documents (Invoices / Packing Lists)")
uploaded_file = st.file_uploader("Upload a file related to an order", type=["pdf", "docx", "jpg", "png"])
if uploaded_file:
    st.success(f"Uploaded file: {uploaded_file.name}")
    st.write("Note: This file is not saved permanently in this demo. Implement cloud storage for production use.")

# --- Download filtered data ---
st.download_button(
    label="📥 Download Filtered Orders as CSV",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="luxvers_filtered_orders.csv",
    mime="text/csv"
)
