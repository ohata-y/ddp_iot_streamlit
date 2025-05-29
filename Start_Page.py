import streamlit as st


st.set_page_config(
    page_title="Start Page", 
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "#### App name"
    }
)


st.write("# Start Page")
st.sidebar.success("Please select a page from above.")

st.markdown("### What's new")
st.markdown(r"2025/--/--: `v1.0.0` released.")

st.markdown("### Note")
st.markdown("""
            Do not use back and forward buttons in your browser.\\
            It may cause unexpected behavior.
            """)
