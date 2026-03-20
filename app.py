# GrocerFlow — app.py
# Main Streamlit app. All UI lives here.

import streamlit as st
import database

items = database.fetch_items(is_deleted=False)
st.write(items)
