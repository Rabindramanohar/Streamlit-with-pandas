import streamlit as st
import pandas as pd

st.set_page_config(page_title="Charts with Streamlit", page_icon=":bar_chart:")
st.title("Charts with Streamlit and Pandas")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if not uploaded_file:
    st.info("Awaiting CSV file to be uploaded.")
    st.stop()

# Read and normalize columns to lowercase to reduce casing issues
df = pd.read_csv(uploaded_file, sep=None, engine='python', on_bad_lines='skip')
df.columns = df.columns.str.strip().str.lower()

# Parse dates and numbers safely
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
else:
    df['date'] = pd.NaT

if 'amount' in df.columns:
    # clean common currency characters before numeric conversion
    df['amount'] = (
        df['amount'].astype(str)
        .str.replace(r'[^0-9\.\-]', '', regex=True)
    )
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
else:
    df['amount'] = pd.NA

# Ensure category exists
if 'category' not in df.columns:
    df['category'] = 'Uncategorized'

# Fill missing amounts with 0 so charts behave
df['amount'] = df['amount'].fillna(0)

# Create a month column (string) for grouping; handle missing dates
df['month'] = df['date'].dt.to_period('M').astype(str)
df.loc[df['date'].isna(), 'month'] = 'Unknown'

left, right = st.columns(2)

with left:
    st.subheader("Spend by category")
    cat = (
        df.groupby('category', as_index=False)['amount']
        .sum()
        .sort_values(by='amount', ascending=False)
    )
    if cat.empty:
        st.info("No category data available to plot.")
    else:
        st.bar_chart(cat, x='category', y='amount', use_container_width=True)

with right:
    st.subheader("Monthly spend")
    monthly = (
        df.groupby('month', as_index=False)['amount']
        .sum()
        .sort_values(by='month')
    )
    if monthly.empty:
        st.info("No monthly data available to plot.")
    else:
        st.line_chart(monthly, x='month', y='amount', use_container_width=True)

