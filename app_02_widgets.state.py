import streamlit as st
import pandas as pd

st.set_page_config(page_title="Forms", page_icon=":memo:")
st.title("Widgets and session State Management")
st.caption("Build a tiny in-memory expense table")

if 'rows' not in st.session_state:
    st.session_state['rows'] = []

st.subheader("Add a new expense")
with st.form("add expense", clear_on_submit=True):
    amount = st.number_input("Amount", min_value=10, step=10, value=100)
    category = st.selectbox("Category", ["Grocery", "Transport", "Rent", "Other"])
    notes = st.text_input("Notes")
    submitted = st.form_submit_button("Add Expense")

if submitted:
    st.session_state.rows.append({"Amount": amount, "Category": category, "Notes": notes})
    st.toast("Expense added!")

st.divider()

st.subheader("Current Momery Table")
df = pd.DataFrame(st.session_state.rows)
if df.empty:
    st.info("No expenses yet. Add some!")
else:
    st.dataframe(df, use_container_width=True)
    st.write(f"**Total Expenses:** ${df['Amount'].sum()}")
                             
