import streamlit as st
import home
import books
import music
import quotes

page_modules = {
    "Home": home,
    "Books": books,
    "Music": music,
    "Quotes": quotes,
}

selected_page = st.sidebar.selectbox("Select a page", page_modules.keys())
page_modules[selected_page].main()