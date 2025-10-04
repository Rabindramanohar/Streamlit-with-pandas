import streamlit as st
st.set_page_config(page_title="Hello World App", page_icon=":wave:")

st.title("Hello, World!")
st.write("""This is your firts Streamlit app!
         You can edit this app in `app_01_hello.py` file.""")
st.subheader("This is a subheader")
st.markdown("""You can use **Markdown** to format your text.
            - **Bold text**
            - *Italic text*
            """) 


name = st.text_input("Enter your name:", "Type here ...")
st.success(f"Hello, {name}! Welcome to your first Streamlit app.")
st.button("Click me!")