import streamlit as st
import pandas as pd

st.set_page_config(page_title="Enhanced file upload and merge", page_icon=":file_folder:")
st.title("Enhanced: Upload and Merge CSV Data with In-Memory Table")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"], accept_multiple_files=True)

dfs = []

def coerce_amount_column(df):
    df = df.copy()
    if "date" in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    if 'amount' in df.columns:
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    return df

if uploaded_file:
    for f in uploaded_file:
        df = pd.read_csv(f, sep=None, engine='python', on_bad_lines='skip')
        df = coerce_amount_column(df)
        dfs.append(df)
        st.success(f"Loaded {len(df)} rows from {f.name}")  

else:
    st.info("Awaiting CSV file(s) to be uploaded.")
    st.stop()

if dfs:
    comfined_df = pd.concat(dfs, ignore_index=True)
    before_rows = len(comfined_df)
    comfined_df = comfined_df.drop_duplicates().reset_index(drop=True)
    after_rows = len(comfined_df)

    st.subheader("Combined Data")
    st.dataframe(comfined_df, use_container_width=True)
    st.write(f"**Total Rows:** {after_rows} (removed {before_rows - after_rows} duplicates)")
    st.download_button(
        label="Download combined data as CSV",
        data=comfined_df.to_csv(index=False).encode('utf-8'),
        file_name='combined_data.csv',
        mime='text/csv'
    )
else:
    st.warning("No valid data to display after processing uploads.")


    