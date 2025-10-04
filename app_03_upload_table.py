import streamlit as st
import pandas as pd

st.set_page_config(page_title="Upload & filter", page_icon=":file_folder:")
st.title("Upload csv and Filter Data")

st.sidebar.header("Filter Options")
min_amt = st.sidebar.number_input("Minimum Amount", min_value=100, step=10)

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file, sep = None, engine='python', on_bad_lines='skip')
    if "date" in df.columns:
        df['date'] = pd.to_datetime(df["date"], errors='coerce')
    if "amount" in df.columns:
        df["amount"] = pd.to_numeric(df["amount"], errors='coerce')

    mask = (df["amount"].fillna(0) >= min_amt)
    df_filtered = df[mask].copy()

    st.success(f"Loaded {len(df)} rows, {len(df_filtered)} after filtering.")
    st.dataframe(df_filtered, use_container_width=True)

    st.download_button(
        label="Download filtered data as CSV",
        data=df_filtered.to_csv(index=False).encode('utf-8'),
        file_name='filtered_data.csv',
        mime='text/csv'
    )   
else:
    st.info("Awaiting CSV file to be uploaded.")
    st.stop()